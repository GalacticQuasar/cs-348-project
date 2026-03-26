from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sales/", views.sales_list, name="sales_list"),
    path("sales/create/", views.sales_create, name="sales_create"),
    path("sales/<int:sale_id>/edit/", views.sales_edit, name="sales_edit"),
    path("sales/<int:sale_id>/delete/", views.sales_delete, name="sales_delete"),
    path("sales/report/", views.sales_report, name="sales_report"),
    path("api/car-models/", views.car_models_by_brand, name="car_models_by_brand"),
]