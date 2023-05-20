from django.urls import path, include
from chat.views import ChatView
from rest_framework import routers
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r"", ChatView)

urlpatterns = [
    path("chatting/", TemplateView.as_view(template_name='chat/index.html')),
    path("", include(router.urls)),
]