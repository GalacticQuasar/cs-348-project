from django.db import models


class Brand(models.Model):
	name = models.CharField(max_length=100, unique=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name


class CarModel(models.Model):
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
	model_name = models.CharField(max_length=100)

	class Meta:
		ordering = ["brand__name", "model_name"]
		constraints = [  # make sure that the model name is unique within the same brand
			models.UniqueConstraint(
				fields=["brand", "model_name"], name="unique_brand_model_name"
			)
		]

	def __str__(self):
		return f"{self.brand.name} - {self.model_name}"


class SalesPerson(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)

	class Meta:
		ordering = ["last_name", "first_name"]

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)

	class Meta:
		ordering = ["last_name", "first_name"]

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


class Sale(models.Model):
	salesperson = models.ForeignKey(
		SalesPerson, on_delete=models.PROTECT, related_name="sales"
	)
	customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="sales")
	car_model = models.ForeignKey(CarModel, on_delete=models.PROTECT, related_name="sales")
	sale_price = models.DecimalField(max_digits=12, decimal_places=2)
	date = models.DateField()

	class Meta:
		ordering = ["-date", "-id"]
		indexes = [  # index by date for faster filtering, and by salesperson and car_model for faster lookups
			models.Index(fields=["date"]),
			models.Index(fields=["salesperson", "date"]),
			models.Index(fields=["car_model"]),
			models.Index(fields=["car_model", "date"]),  # add composite index for car_model and date to speed up report queries that filter by both
		]

	def __str__(self):
		return f"Sale #{self.id} - {self.car_model} - ${self.sale_price}"
