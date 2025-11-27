from django.db import models
from core.models import Customer


class Subscription(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	plan = models.CharField(max_length=100)
	start_date = models.DateField()
	end_date = models.DateField(blank=True, null=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.customer} - {self.plan}"
