from django.db import models

class TRANSACTION_STATUS(models.IntegerChoices):
    PENDING = 1, "pending"
    PAID = 2, "paid"
    FAILED = 3, "failed"
    WITHDRAWAL_REQUEST_DENIED = 4, "withdrawal request denied"

class TRANSACTION_TYPE(models.IntegerChoices):
    RENT_PAYMENT = 1, "payment from rent"
    WITHDRAWAL = 2, "payment from withdrawal"