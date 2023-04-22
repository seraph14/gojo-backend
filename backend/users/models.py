from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
from users.utilities import UserTypes

class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    role = models.IntegerField(choices=UserTypes.choices, default=UserTypes.TENANT)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",]

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email
    

