from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from chat.serializers import ThreadSerializer, MessageSerializer
from chat.models import Thread, Message
from users.permissions import IsLandlord, IsManager, CanEditPropertyDetail, CanCreateProperty


class ChatView(
    viewsets.ModelViewSet
):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all().prefetch_related('messages')
    lookup_field = "pk"

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        # Create a thread
        message = Message.objects.create(
            thread=Thread.objects.create(
                user_1=user,
                user_2=data["to"]
            ),
            sender=user,
            content=data["message"],
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_200_OK)
