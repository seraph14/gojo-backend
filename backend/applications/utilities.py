from django.db import models

class APPLICATION_STATUS(models.IntegerChoices):
    PENDING = 0
    APPROVED = 1
    WITHDRAWN = 2
    REJECTED = 3