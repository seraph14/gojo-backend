from django.db import models

class TRANSACTION_STATUS(models.IntegerChoices):
    PENDING = 1, "pending"
    PAID = 2, "paid"
    FAILED = 3, "failed"
    WITHDRAWAL_REQUEST_APPROVED = 4, "Withdrawal approved"
    WITHDRAWAL_REQUEST_DENIED = 5, "Withdrawal denied"

class TRANSACTION_TYPE(models.IntegerChoices):
    RENT_PAYMENT = 1, "payment from rent"
    WITHDRAWAL = 2, "payment from withdrawal"

def validate_withdrawal_request(transaction):
    from transactions.models import Transaction
    from transactions.utils import TRANSACTION_STATUS, TRANSACTION_TYPE
    
    if withdrawal_request.type != TRANSACTION_TYPE.WITHDRAWAL:
        return False
    if withdrawal_request.status == TRANSACTION_STATUS.PENDING:
        return True
    return False