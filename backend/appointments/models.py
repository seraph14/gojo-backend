from django.db import models
from appointments.utils import APPOINTMENT_STATUS
from users.models import User
from properties.models import Property

class Appointment(models.Model):
    status = models.IntegerField(choices=APPOINTMENT_STATUS.choices, default=APPOINTMENT_STATUS.PENDING)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
