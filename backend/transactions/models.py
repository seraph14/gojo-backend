from django.db import models
from users.models import User
from properties.models import Property

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_transactions')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="transactions")
    description = models.TextField()
    status = models.IntegerField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} - {self.amount}'