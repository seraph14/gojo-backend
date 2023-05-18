from django.urls import path, include
from chat.views import ChatView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", ChatView)

urlpatterns = [
    path("", include(router.urls)),
]