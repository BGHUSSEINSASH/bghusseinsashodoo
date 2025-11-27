from django.db import models


class SignatureRequest(models.Model):
    document_title = models.CharField(max_length=255)
    recipient_email = models.EmailField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document_title
