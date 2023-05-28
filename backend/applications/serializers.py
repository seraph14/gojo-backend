from rest_framework import serializers
from applications.models import Application
from applications.utilities import APPLICATION_STATUS
from users.serializers import BasicUserSerializer
from properties.serializers import BasicPropertySerializer


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ApplicationViewSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    tenant = BasicUserSerializer()
    property = BasicPropertySerializer()
    possible_start_date = serializers.DateField(format="%d/%m/%Y")
    
    def get_status(self, obj):
        return APPLICATION_STATUS(obj.status).label
        
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')