import uuid
from django.db import models
from users.models import User
from properties.models import Property
from transactions.utils import TRANSACTION_STATUS, TRANSACTION_TYPE

# TODO: move this to a different file
class PROPERTY_RENT_STATUS(models.IntegerChoices):
    ONGOING = 1, "still renting"
    ENDED = 2, "rent completed"

# FIXME: move this to a different file
class UserRentedProperties(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="property_renter")
    start_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_rented_properties")
    status = models.IntegerField(default=PROPERTY_RENT_STATUS.ONGOING, choices=PROPERTY_RENT_STATUS.choices)

class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_transactions', null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_transactions', null=True, blank=True)
    # FIXME: what is the difference between amount and payment_rate
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    tx_ref = models.UUIDField(auto_created=True, default=uuid.uuid4)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    checkout_url = models.CharField(max_length=500, null=True, blank=True)

    status = models.IntegerField(default=TRANSACTION_STATUS.PENDING, choices=TRANSACTION_STATUS.choices)
    rent_detail = models.ForeignKey(UserRentedProperties, on_delete=models.CASCADE, related_name="transactions", null=True, blank=True)
    type = models.IntegerField(default=TRANSACTION_TYPE.RENT_PAYMENT, choices=TRANSACTION_TYPE.choices)
    
    bank_detail = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} - {self.amount}'

    class Meta:
        ordering = ["-payment_date"]
