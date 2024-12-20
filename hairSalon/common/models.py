from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        permissions = [
            ("add_service", "Can add service"),
            ("change_service", "Can change service"),
            ("delete_service", "Can delete service"),
        ]

    def __str__(self):
        return f"{self.name} - ${self.price}"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
