from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

class Property(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    availability = models.IntegerField(_("availability"),)
    category = ArrayField(
        models.IntegerField(),
    ) 
    # TODO: virtual_tour
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    facilities = ArrayField(
        models.CharField(max_length=200),
        default=list
    )

