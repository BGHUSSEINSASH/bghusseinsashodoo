from django.db import models
from core.models import Employee


class Message(models.Model):
    sender = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}"
