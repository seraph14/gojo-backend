from datetime import timedelta
from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from appointments.models import Appointment
from appointments.utils import APPOINTMENT_STATUS
from properties.serializers import PropertySerializer
from users.serializers import BasicUserSerializer


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
 

class AppointmentViewSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    # tenant = BasicUserSerializer()
    
    # property = PropertySerializer()
    date = serializers.DateTimeField(format="%b %d, %I:%M %p", source="appointment_date")

    landlord_phone = serializers.SerializerMethodField()
    landlord_full_name = serializers.SerializerMethodField()

    def get_landlord_phone(self, obj):
        return obj.property.owner.phone

    def get_landlord_full_name(self, obj):
        return obj.property.owner.full_name

    def get_status(self, obj):
        return APPOINTMENT_STATUS(obj.status).label
        
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')