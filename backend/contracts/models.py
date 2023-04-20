from django.db import models
from properties.models import Property
from users.models import User


class Contact(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_image = models.ImageField(upload_to='contracts', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)