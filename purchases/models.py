from django.db import models
from core.models import Supplier


class PurchaseOrder(models.Model):
	STATUS_CHOICES = [
		("draft", "Draft"),
		("confirmed", "Confirmed"),
		("received", "Received"),
		("billed", "Billed"),
		("cancelled", "Cancelled"),
	]

	number = models.CharField(max_length=50, unique=True)
	supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
	date = models.DateField()
	total = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

	def __str__(self):
		return self.number
