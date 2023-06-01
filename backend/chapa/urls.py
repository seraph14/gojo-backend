from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from chapa.views import verify_payment_status

urlpatterns = [
    path("verify_payment_status/", verify_payment_status, name="verify_payment_status"),
]