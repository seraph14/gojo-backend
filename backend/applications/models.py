from django.db import models
from users.models import User
from properties.models import Property
from applications.utilities import ApplicationStatus

class Application(models.Model):
    
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications_by_tenant")
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications_by_landlord")
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=ApplicationStatus.choices)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tenant.email + " - " + self.property.title

    class Meta:
        ordering = ["-id"]