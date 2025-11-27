from django.db import models


class MaintenanceRequest(models.Model):
	title = models.CharField(max_length=255)
	equipment = models.CharField(max_length=255, blank=True, null=True)
	status = models.CharField(max_length=20, default='open')
	request_date = models.DateField()

	def __str__(self):
		return self.title
