from rest_framework import serializers
from properties.models import Property
from users.serializers import UserSerializer
from users.models import User
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id",)