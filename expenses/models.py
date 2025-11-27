from django.db import models
from core.models import Employee


class ExpenseReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.employee} - {self.description}"
