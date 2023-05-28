from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User
from users.utilities import UserTypes

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=UserTypes.choices, default=UserTypes.TENANT)
    is_active = serializers.BooleanField(default=False)
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    class Meta:
        model = User 
        fields = ["id",  "first_name", "last_name", "role" , "password", "avatar", "phone", "identification", "is_active"]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}, 'is_active': { 'read_only': True } }


# TODO: which part of the code this affects [there used to be [BasicUserSerializerForChat]
class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["id", "avatar", "phone", "first_name", "last_name"]
        extra_kwargs = {'id': { 'read_only': True } }
