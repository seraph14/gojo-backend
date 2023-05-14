from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User
from users.utilities import UserTypes

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=UserTypes.choices)
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    class Meta:
        model = User 
        fields = ["id",  "first_name", "last_name", "role" ,"email", "password", "avatar", "phone"]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}