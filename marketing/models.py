from django.db import models


class Campaign(models.Model):
	name = models.CharField(max_length=255)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)

	def __str__(self):
		return self.name


class Lead(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	source = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.name
