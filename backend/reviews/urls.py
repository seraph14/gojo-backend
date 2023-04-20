from django.urls import path, include
from reviews.views import ReviewView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", ReviewView)

urlpatterns = [
    path("", include(router.urls)),
]