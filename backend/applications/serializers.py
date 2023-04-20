from rest_framework import serializers
from users.serializers import UserSerializer
from applications.models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')