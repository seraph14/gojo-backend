from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

class Category(models.Model):
    name = models.CharField(max_length=256)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Facility(models.Model):
    name = models.CharField(max_length=256)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    availability = ArrayField(
        models.DateTimeField()
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    # TODO: virtual_tour

    is_approved = models.BooleanField(default=False)
    # FIXME: If you have time rename this field to price
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['-id']

class PropertyImage(models.Model):
    image = models.ImageField(upload_to="property_images/")
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)


class PropertyFacility(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="facilities")
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="properties")
    count = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.property.name} - {self.facility.name}"


class PropertyLocation(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="location")
    name = models.CharField(max_length=800, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
