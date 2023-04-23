from django.db import models


class UserTypes(models.IntegerChoices):
    TENANT = 1
    LANDLORD = 2
    FINANCIAL_MANAGER = 3
    LISTING_MANAGER = 4
    GENERAL_MANAGER = 5