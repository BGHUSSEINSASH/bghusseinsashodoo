from django.db import models
from core.models import Product, Warehouse


class StockMove(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.DecimalField(max_digits=12, decimal_places=2)
	from_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, related_name='moves_out')
	to_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, related_name='moves_in')
	date = models.DateTimeField()

	def __str__(self):
		return f"{self.product} {self.quantity}"
