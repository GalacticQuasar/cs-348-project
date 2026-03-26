from django.contrib import admin
from .models import Brand, CarModel, Customer, Sale, SalesPerson


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
	list_display = ("id", "brand", "model_name")
	list_filter = ("brand",)
	search_fields = ("model_name", "brand__name")


@admin.register(SalesPerson)
class SalesPersonAdmin(admin.ModelAdmin):
	list_display = ("id", "first_name", "last_name")
	search_fields = ("first_name", "last_name")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ("id", "first_name", "last_name", "email")
	search_fields = ("first_name", "last_name", "email")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
	list_display = ("id", "date", "salesperson", "customer", "car_model", "sale_price")
	list_filter = ("date", "salesperson", "car_model__brand")
	search_fields = (
		"salesperson__first_name",
		"salesperson__last_name",
		"customer__first_name",
		"customer__last_name",
		"car_model__model_name",
		"car_model__brand__name",
	)
