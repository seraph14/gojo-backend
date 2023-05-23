from rest_framework import serializers
from properties.models import Property, PropertyImage, Category
from users.serializers import UserSerializer
from users.models import User
from users.serializers import UserSerializer 
class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    owner = UserSerializer()
    categories = CategorySerializer(many=True, required=False)
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id",)


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"