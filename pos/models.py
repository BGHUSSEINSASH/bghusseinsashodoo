from django.db import models
from core.models import Customer


class POSOrder(models.Model):
	number = models.CharField(max_length=50, unique=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date = models.DateTimeField()
	total = models.DecimalField(max_digits=12, decimal_places=2)
	status = models.CharField(max_length=20, default='draft')

	def __str__(self):
		return self.number
