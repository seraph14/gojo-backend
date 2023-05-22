from rest_framework import serializers
from chat.models import Thread, Message
from users.serializers import UserSerializer, BasicUserSerializer
from users.models import User
from datetime import datetime, timedelta
from django.utils import timezone


class CustomTimestampField(serializers.DateTimeField):
    def to_representation(self, value):
        now = timezone.now()
        if value >= now - timedelta(days=1):
            # Display the time for dates within the last 24 hours
            return value.strftime("%H:%M")
        elif value >= now - timedelta(days=7):
            # Display the weekday for dates within the last 7 days
            return value.strftime("%a %H:%M")
        else:
            # Display the full date for dates before the past 7 days
            return value.strftime("%b %d, %H:%M")


class MessageSerializer(serializers.ModelSerializer):
    sender = BasicUserSerializer()
    timestamp = CustomTimestampField()
    class Meta:
        model = Message
        fields = ["content", "sender", "timestamp", "seen"]
        read_only_fields = ("id",)

class ThreadSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    user_1 = BasicUserSerializer()
    user_2 = BasicUserSerializer()
    unseen_count = serializers.SerializerMethodField()

    def get_unseen_count(self, obj):
        return 0

    def get_messages(self, obj):
        return MessageSerializer(Message.objects.all(), many=True).data

    class Meta:
        model = Thread
        fields = "__all__"
