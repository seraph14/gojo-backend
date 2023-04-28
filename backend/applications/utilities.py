from django.db import models

class ApplicationStatus(models.IntegerChoices):
    PENDING = 0
    SIGNED = 1
    REVOKED = 2