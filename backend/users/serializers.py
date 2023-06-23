import os
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User, AccountBalance
from users.utilities import UserTypes

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=UserTypes.choices, default=UserTypes.TENANT)
    is_active = serializers.BooleanField(default=False)

    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        if obj.avatar:
            return str(os.environ.get("DOMAIN", "http://localhost:8000")) + "/" + str(
                obj.avatar
            )

        return None
     
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    class Meta:
        model = User 
        fields = ["id",  "first_name", "last_name", "role" , "password", "avatar", "phone", "identification", "is_active", "picture"]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}, 'is_active': { 'read_only': True } }


# TODO: which part of the code this affects [there used to be [BasicUserSerializerForChat]
class BasicUserSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField()

    def get_picture(self, obj):
        if obj.avatar:
            return str(os.environ.get("DOMAIN", "http://localhost:8000")) + "/" + str(
                obj.avatar
            )

        return None
     

    class Meta:
        model = User 
        fields = ["id", "avatar", "phone", "first_name", "last_name", "picture", "full_name"]
        extra_kwargs = {'id': { 'read_only': True } }

class AccountBalanceSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, coerce_to_string=False)
    class Meta:
        model = AccountBalance
        fields = ["amount"]