from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.title
