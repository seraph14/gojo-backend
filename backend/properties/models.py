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

    # TODO: replace this with address object { street: "", "longitude": 12312, "latitude": 12312 }
    address = models.JSONField(default=dict, )
    # TODO: Refactor this and remove it
    
    # latitude = models.DecimalField(max_digits=9, decimal_places=6)
    # longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    is_approved = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ['-id']

class PropertyImage(models.Model):
    image = models.ImageField(upload_to="property_images/")
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)


class PropertyFacility(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="facilities")
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="properties")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.property.name} - {self.facility.name}"

# TODO: property Appointment
class PropertyAppointment:
    '''
        Appointment(
        phoneNumber: "0911234532",
        id: "1",
        fullName: "Braha Marlam Roh I",
        date: "March 21, 2023",
        ),
    '''
    pass