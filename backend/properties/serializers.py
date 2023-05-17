from rest_framework import serializers
from properties.models import Property, PropertyImage
from users.serializers import UserSerializer
from users.models import User
from users.serializers import UserSerializer 
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    owner = UserSerializer()
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id",)