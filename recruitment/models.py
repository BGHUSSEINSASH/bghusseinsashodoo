from django.db import models


class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_date = models.DateField()
    status = models.CharField(max_length=20, default='open')

    def __str__(self):
        return self.title
