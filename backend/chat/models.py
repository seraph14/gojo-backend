from django.db import models
from users.models import User


class Thread(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tenant_threads")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="landlord_threads")

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.id}'
