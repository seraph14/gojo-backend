# chat/routing.py

from django.urls import re_path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>[\w.@+-]+)/', ChatConsumer.as_asgi())
    # re_path(r'ws/chat/', ChatConsumer.as_asgi()),
]