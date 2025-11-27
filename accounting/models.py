from django.db import models
from core.models import Customer


class Invoice(models.Model):
	STATUS_CHOICES = [
		("draft", "Draft"),
		("posted", "Posted"),
		("paid", "Paid"),
		("cancelled", "Cancelled"),
	]

	number = models.CharField(max_length=50, unique=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateField()
	total = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

	def __str__(self):
		return self.number


class Expense(models.Model):
	description = models.CharField(max_length=255)
	amount = models.DecimalField(max_digits=12, decimal_places=2)
	date = models.DateField()

	def __str__(self):
		return f"{self.description} - {self.amount}"
