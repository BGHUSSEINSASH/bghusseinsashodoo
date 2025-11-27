from django.db import models
from core.models import Employee


class Project(models.Model):
	name = models.CharField(max_length=255)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.name


class Task(models.Model):
	STATUS_CHOICES = [("todo", "To Do"), ("doing", "In Progress"), ("done", "Done")]

	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
	due_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.title
