from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from chat.serializers import ThreadSerializer, MessageSerializer
from chat.models import Thread, Message
from users.permissions import IsLandlord, IsManager, CanEditPropertyDetail, CanCreateProperty


class ChatView(
    viewsets.ModelViewSet
):
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all().prefetch_related('messages')
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        if self.action == "list":
            return Thread.objects.filter(user_1=self.request.user).union(
                Thread.objects.filter(user_2=self.request.user)
            )
        return super().get_queryset()

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

