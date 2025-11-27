from django.db import models
from core.models import Customer


class SalesOrder(models.Model):
	STATUS_CHOICES = [
		("draft", "Draft"),
		("confirmed", "Confirmed"),
		("delivered", "Delivered"),
		("invoiced", "Invoiced"),
		("cancelled", "Cancelled"),
	]

	number = models.CharField(max_length=50, unique=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateField()
	total = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

	def __str__(self):
		return self.number


class Quote(models.Model):
	number = models.CharField(max_length=50, unique=True)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date = models.DateField()
	total = models.DecimalField(max_digits=12, decimal_places=2)

	def __str__(self):
		return self.number
