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
    avatar = models.ImageField(upload_to="avatar/", null=True)
    identification = models.ImageField(upload_to="id_img/", null=True)
    phone = models.CharField(_('phone number'), null=True, max_length=10)
    is_verified = models.BooleanField(_("is verified"),default=False)
    phone_verified = models.BooleanField(_("is phone number verified"), default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",]

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-id']