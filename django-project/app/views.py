from django.contrib import messages
from django.db import transaction
from django.db.models import Avg, Count, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SaleForm, SalesReportFilterForm
from .models import CarModel, Sale


def index(request):
    return render(request, "index.html")

# Endpoints for CRUD operations for Sale model and serving sales report
def sales_list(request):
    sales = (
        Sale.objects.select_related("salesperson", "customer", "car_model", "car_model__brand")
        .all()
        .order_by("-date", "-id")  # order by date desc (so newest sales are at the top)
    )
    return render(request, "sales_list.html", {"sales": sales})


def sales_create(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, "Sale created successfully.")
            return redirect("sales_list")
    else:
        form = SaleForm()

    return render(request, "sales_form.html", {"form": form, "page_title": "Add Sale"})


def sales_edit(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)

    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            messages.success(request, "Sale updated successfully.")
            return redirect("sales_list")
    else:
        form = SaleForm(instance=sale)

    return render(
        request,
        "sales_form.html",
        {
            "form": form,
            "page_title": f"Edit Sale #{sale.id}",
            "sale": sale,
        },
    )


def sales_delete(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)

    if request.method == "POST":
        with transaction.atomic():
            sale.delete()
        messages.success(request, "Sale deleted successfully.")
        return redirect("sales_list")

    return render(request, "sales_delete_confirm.html", {"sale": sale})


def sales_report(request):
    form = SalesReportFilterForm(request.GET or None)
    sales = Sale.objects.select_related(
        "salesperson", "customer", "car_model", "car_model__brand"
    ).all()

    if form.is_valid():
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        salesperson = form.cleaned_data.get("salesperson")
        brand = form.cleaned_data.get("brand")

        if start_date:
            sales = sales.filter(date__gte=start_date)
        if end_date:
            sales = sales.filter(date__lte=end_date)
        if salesperson:
            sales = sales.filter(salesperson=salesperson)
        if brand:
            sales = sales.filter(car_model__brand=brand)

    stats = sales.aggregate(
        total_sales_amount=Sum("sale_price"),
        average_sale_price=Avg("sale_price"),
        total_number_of_sales=Count("id"),
    )
    brand_breakdown = (
        sales.values("car_model__brand__name")
        .annotate(
            sales_count=Count("id"),
            brand_total=Sum("sale_price"),
            brand_average=Avg("sale_price"),
        )
        .order_by("car_model__brand__name")
    )

    return render(
        request,
        "sales_report.html",
        {
            "form": form,
            "sales": sales.order_by("-date", "-id"),
            "stats": stats,
            "brand_breakdown": brand_breakdown,
        },
    )


def car_models_by_brand(request):
    brand_id = request.GET.get("brand_id")
    if not brand_id:
        return JsonResponse({"models": []}, status=400)

    try:
        brand_id = int(brand_id)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid brand_id: must be an integer."}, status=400)

    if brand_id < 1:
        return JsonResponse({"error": "Invalid brand_id: must be a positive integer."}, status=400)

    models_qs = CarModel.objects.filter(brand_id=brand_id).order_by("model_name")
    models_data = [{"id": model.id, "name": model.model_name} for model in models_qs]
    return JsonResponse({"models": models_data})