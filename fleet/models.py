from django.db import models


class Vehicle(models.Model):
    plate_number = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"{self.plate_number} - {self.brand} {self.model}"
