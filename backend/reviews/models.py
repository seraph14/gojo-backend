from django.db import models
from properties.models import Property
from users.models import User


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return self.by.email

    class Meta:
         ordering = ("-date",)