import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hairSalon.settings')
django.setup()

from hairSalon.common.models import Service

services = [
    ("Haircut", "A standard haircut", 25.00),
    ("Hair Color", "Hair coloring service", 50.00),
    ("Beard Trim", "Trim your beard", 15.00),
]


def populate_services():
    for name, description, price in services:
        service, created = Service.objects.get_or_create(
            name=name,
            defaults={"description": description, "price": price},
        )
        if created:
            print(f"Created service: {name}")
        else:
            service.description = description
            service.price = price
            service.save()
            print(f"Updated service: {name}")


if __name__ == "__main__":
    populate_services()
