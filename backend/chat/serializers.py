from rest_framework import serializers
from chat.models import Thread, Message
from users.serializers import UserSerializer
from users.models import User

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Message
        fields = ["content", "sender", "timestamp", "seen"]
        read_only_fields = ("id",)

class ThreadSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    def get_messages(self):
        return MessageSerializer(Message.objects.all()).data

    class Meta:
        model = Thread
        fields = "__all__"
