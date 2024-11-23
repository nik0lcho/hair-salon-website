from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.DurationField(help_text="Estimated time required for the service")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price}|{self.duration}"
