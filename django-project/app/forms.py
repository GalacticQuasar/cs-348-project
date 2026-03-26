from django import forms

from .models import Brand, CarModel, Sale, SalesPerson


class SaleForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.none(), required=True)

    class Meta:
        model = Sale
        fields = ["date", "salesperson", "customer", "brand", "car_model", "sale_price"]
        widgets = {  # we want to use date picker so it's easier for the user to select date
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["brand"].queryset = Brand.objects.all().order_by("name")  # populate brand dropdown from db
        self.fields["salesperson"].queryset = SalesPerson.objects.all().order_by(  # populate salesperson dropdown from db
            "last_name", "first_name"
        )

        selected_brand = None
        if self.data.get("brand"):
            try:
                selected_brand = int(self.data.get("brand"))
            except (TypeError, ValueError):
                selected_brand = None
        elif self.instance.pk:
            selected_brand = self.instance.car_model.brand_id

        if selected_brand is not None:  # dynamically filter car models based on selected brand
            self.fields["car_model"].queryset = CarModel.objects.filter(  # SELECT * FROM CarModel WHERE brand_id = selected_brand ORDER BY model_name
                brand_id=selected_brand
            ).order_by("model_name")
            self.fields["brand"].initial = selected_brand
        else:
            self.fields["car_model"].queryset = CarModel.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        brand = cleaned_data.get("brand")
        car_model = cleaned_data.get("car_model")

        if brand and car_model and car_model.brand_id != brand.id:  # validate that the selected model belongs to the selected brand
            self.add_error(
                "car_model", "Selected model does not belong to the selected brand."
            )

        return cleaned_data


class SalesReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    salesperson = forms.ModelChoiceField(
        queryset=SalesPerson.objects.all().order_by("last_name", "first_name"),
        required=False,
        empty_label="All salespeople",
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all().order_by("name"),
        required=False,
        empty_label="All brands",
    )
