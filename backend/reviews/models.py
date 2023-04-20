from django.db import models
from properties.models import Property
from users.models import User


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return self.by.email