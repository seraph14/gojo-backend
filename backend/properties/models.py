from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = ArrayField(
        models.DateTimeField()
    )
    category = ArrayField(
        models.IntegerField(),
    )
    # TODO: virtual_tour
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    facilities = models.JSONField(default=dict, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

class PropertyImage(models.Model):
    image = models.ImageField(upload_to="property_images/")
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)