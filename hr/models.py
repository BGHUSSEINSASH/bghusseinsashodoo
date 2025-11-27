from django.db import models
from core.models import Employee


class Attendance(models.Model):
	STATUS_CHOICES = [("present", "Present"), ("absent", "Absent"), ("late", "Late")]

	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	date = models.DateField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES)

	def __str__(self):
		return f"{self.employee} {self.date} {self.status}"


class Payroll(models.Model):
	employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
	period = models.CharField(max_length=20)  # e.g., 2025-11
	amount = models.DecimalField(max_digits=12, decimal_places=2)

	def __str__(self):
		return f"{self.employee} {self.period}"
