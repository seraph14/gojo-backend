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
            return value.strftime("%b %d, %Y")


class MessageSerializer(serializers.ModelSerializer):
    sender = BasicUserSerializer()
    timestamp = CustomTimestampField()
    class Meta:
        model = Message
        fields = ["content", "sender", "timestamp", "seen"]
        read_only_fields = ("id",)



class MessageViewSerializer(serializers.ModelSerializer):
    from_me = serializers.SerializerMethodField()
    sender = BasicUserSerializer()
    timestamp = CustomTimestampField()

    def get_from_me(self, obj):
        user = self.context['request'].user
        return user.id == obj.sender.id
    
    class Meta:
        model = Message
        fields = ["content", "sender", "timestamp", "seen", "from_me"]
        read_only_fields = ("id",)


class ThreadSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    tenant = BasicUserSerializer(source="user_1")
    landlord = BasicUserSerializer(source="user_2")
    unseen_count = serializers.SerializerMethodField()

    def get_unseen_count(self, obj):
        return 0

    def get_messages(self, obj):
        return MessageViewSerializer(Message.objects.all(), many=True, context=self.context).data

    class Meta:
        model = Thread
        fields = [ "id", "messages", "tenant", "landlord", "unseen_count"]
