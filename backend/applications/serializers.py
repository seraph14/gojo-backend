from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from applications.models import Application, Contract
from applications.utilities import APPLICATION_STATUS
from users.serializers import BasicUserSerializer


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class ApplicationViewSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    tenant = BasicUserSerializer()
    property_title = serializers.CharField(source="property.title")
    property_thumbnail_url = serializers.SerializerMethodField()
    possible_start_date = serializers.DateField("%b %d, %Y")
    possible_end_date = serializers.SerializerMethodField()
    application_date = serializers.DateField("%b %d, %Y")

    def get_property_thumbnail_url(self, obj):
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTooc7RcJtAj9LLZyHrnxkx_jlzFmT12YAy6bLt3eYRLnoYXV_cqSBg1SUcPDRq8fHzXKI&usqp=CAU"

    def get_possible_end_date(self, obj):
        months = relativedelta(months=obj.how_long)
        possible_end_date = obj.possible_start_date + months
        return possible_end_date.strftime("%b %d, %Y")

    def get_status(self, obj):
        return APPLICATION_STATUS(obj.status).label
        
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
