from django.db import models
from core.models import Product


class WorkOrder(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.DecimalField(max_digits=12, decimal_places=2)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	status = models.CharField(max_length=20, default='planned')

	def __str__(self):
		return f"WO {self.product} x {self.quantity}"
