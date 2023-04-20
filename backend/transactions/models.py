from django.db import models
from users.models import User


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status = models.IntegerField(default=False)

    def __str__(self):
        return f'{self.sender} to {self.receiver} - {self.amount}'