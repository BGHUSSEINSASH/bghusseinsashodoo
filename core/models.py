from django.db import models


class TimestampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Customer(TimestampedModel):
	name = models.CharField(max_length=255)
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	address = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name


class Supplier(TimestampedModel):
	name = models.CharField(max_length=255)
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	address = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name


class Warehouse(TimestampedModel):
	name = models.CharField(max_length=255)
	location = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.name


class Product(TimestampedModel):
	sku = models.CharField(max_length=100, unique=True)
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)

	def __str__(self):
		return f"{self.sku} - {self.name}"


class Employee(TimestampedModel):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(blank=True, null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)
	position = models.CharField(max_length=100, blank=True, null=True)
	hire_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name}"
