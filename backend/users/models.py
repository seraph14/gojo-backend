from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager
from users.utilities import UserTypes

class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    role = models.IntegerField(choices=UserTypes.choices, default=UserTypes.TENANT)
    avatar = models.ImageField(upload_to="avatar/", null=True)
    identification = models.ImageField(upload_to="id_img/", null=True)
    phone = models.CharField(_('phone number'), unique=True, max_length=10)
    is_verified = models.BooleanField(_("is verified"),default=False)

    # FIXME: see if there is a better approach for this
    fb_registration_token = models.CharField(max_length=600, default="__empty__")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name",]

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-id']

class UserVerification(models.Model):
    request_id = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(User, related_name='otp_status', on_delete=models.CASCADE)

class AccountBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="balance")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
