from django.db import models


class UserTypes(models.IntegerChoices):
    TENANT = 1
    LANDLORD = 2
    GENERAL_MANAGER = 3
    LISTING_MANAGER = 4
    FINANCIAL_MANAGER = 5