from django.db import models

class APPOINTMENT_STATUS(models.IntegerChoices):
    PENDING = 0, "pending"
    APPROVED = 1, "approved"
    # FIXME: assume rejected is cancelled
    REJECTED = 2, "rejected"
    CANCELED = 3, "canceled"