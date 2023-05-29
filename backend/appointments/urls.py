from django.urls import path, include
from appointments.views import AppointmentView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', AppointmentView)

urlpatterns = [
    path('', include(router.urls), name="appointments"),
]
