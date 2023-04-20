from django.urls import path, include
from applications.views import ApplicationView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', ApplicationView)

urlpatterns = [
    path('', include(router.urls)),
]