from django.db import models


class EmailCampaign(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    sent_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name
