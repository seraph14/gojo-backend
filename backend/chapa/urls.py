from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from chapa.views import get_chapa_checkout_url

urlpatterns = [
    path("get_chapa_checkout_url/", get_chapa_checkout_url, name="get_chapa_checkout_url"),
]