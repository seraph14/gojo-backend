from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    class Meta:
        model = User 
        fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}