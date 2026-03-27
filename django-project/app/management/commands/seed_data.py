from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from app.models import Brand, CarModel, Customer, Sale, SalesPerson


class Command(BaseCommand):
    help = "Seed sample dealership data"

    def handle(self, *args, **options):
        brands_data = {
            "Toyota": ["Corolla", "Camry", "RAV4"],
            "Honda": ["Civic", "Accord", "CR-V"],
            "Ford": ["F-150", "Escape", "Mustang"],
        }

        models = {}
        for brand_name, model_names in brands_data.items():
            brand, _ = Brand.objects.get_or_create(name=brand_name)
            for model_name in model_names:
                car_model, _ = CarModel.objects.get_or_create(
                    brand=brand, model_name=model_name
                )
                models[f"{brand_name}:{model_name}"] = car_model

        salespeople = []
        for first_name, last_name in [
            ("Alex", "Nguyen"),
            ("Priya", "Patel"),
            ("Marcus", "Lee"),
        ]:
            salesperson, _ = SalesPerson.objects.get_or_create(
                first_name=first_name, last_name=last_name
            )
            salespeople.append(salesperson)

        customers = []
        for first_name, last_name, email in [
            ("Emma", "Stone", "emma.stone@example.com"),
            ("Noah", "Baker", "noah.baker@example.com"),
            ("Mia", "Kim", "mia.kim@example.com"),
            ("Liam", "Davis", "liam.davis@example.com"),
        ]:
            customer, _ = Customer.objects.get_or_create(
                email=email,
                defaults={"first_name": first_name, "last_name": last_name},
            )
            customers.append(customer)

        sales_templates = [
            ("Toyota:Corolla", 21999.00, 2),
            ("Honda:Civic", 23450.00, 10),
            ("Ford:Escape", 28750.00, 20),
            ("Toyota:RAV4", 31200.00, 35),
            ("Honda:Accord", 26990.00, 50),
            ("Ford:Mustang", 40200.00, 65),
        ]

        created = 0
        for index, (model_key, price, days_ago) in enumerate(sales_templates):
            sale_date = date.today() - timedelta(days=days_ago)
            salesperson = salespeople[index % len(salespeople)]
            customer = customers[index % len(customers)]
            car_model = models[model_key]

            sale, was_created = Sale.objects.get_or_create(
                date=sale_date,
                salesperson=salesperson,
                customer=customer,
                car_model=car_model,
                defaults={"sale_price": Decimal(str(price))},
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Brands={Brand.objects.count()}, Models={CarModel.objects.count()}, Sales={Sale.objects.count()}, New sales={created}"
            )
        )
