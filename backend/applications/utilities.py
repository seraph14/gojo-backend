from django.db import models

class APPLICATION_STATUS(models.IntegerChoices):
    PENDING = 0, "pending"
    APPROVED = 1, "approved"
    WITHDRAWN = 2, "withdrawn"
    REJECTED = 3, "rejected"