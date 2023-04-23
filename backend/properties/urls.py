from django.urls import path, include
from properties.views import PropertyView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", PropertyView)

urlpatterns = [
    path("", include(router.urls)),
]