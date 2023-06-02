from django.db import models
from users.models import User
from properties.models import Property
from applications.utilities import APPLICATION_STATUS

class Application(models.Model):
    
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications_by_tenant")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="applications")
    possible_start_date = models.DateField()
    how_long = models.IntegerField(default=1)
    status = models.IntegerField(default=APPLICATION_STATUS.PENDING, choices=APPLICATION_STATUS.choices)
    description = models.TextField()
    application_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tenant.email + " - " + self.property.title

    class Meta:
        ordering = ["application_date"]