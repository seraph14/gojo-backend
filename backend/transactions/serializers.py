from rest_framework import serializers
from users.models import User
from transactions.models import Transaction, UserRentedProperties, PROPERTY_RENT_STATUS
from properties.serializers import PropertySerializer, PropertyImageSerializer
from users.serializers import BasicUserSerializer
from transactions.utils import TRANSACTION_STATUS, TRANSACTION_TYPE
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class UserRentedPropertySerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    user = BasicUserSerializer()
    status = serializers.SerializerMethodField()


    def get_status(self, obj):
        return PROPERTY_RENT_STATUS(obj.status).label

    class Meta:
        model = UserRentedProperties
        fields = "__all__"



class TransactionTenantSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateTimeField(format="%d/%m/%Y")
    property_title = serializers.SerializerMethodField()
    property_image = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    def get_property_title(self, obj):
        print("====================", obj)
        if obj.rent_detail is not None:
            return obj.rent_detail.property.title
        return ""
        
    def get_property_image(self, obj):
        # image_data = PropertyImageSerializer(obj.images.first(),context=self.context)
        # if len(image_data.data) != 0:
            # return image_data.data["image"]
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTooc7RcJtAj9LLZyHrnxkx_jlzFmT12YAy6bLt3eYRLnoYXV_cqSBg1SUcPDRq8fHzXKI&usqp=CAU"
   
    def get_status(self, obj):
        return TRANSACTION_STATUS(obj.status).label

    def get_type(self, obj):
        return TRANSACTION_TYPE(obj.type).label

    class Meta:
        model = Transaction
        fields = [
            "id",
            "property_title",   
            "property_image",   
            "payment_date",
            "status",
            "amount"
        ]




class TransactionLandlordSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_status(self, obj):
        return TRANSACTION_STATUS(obj.status).label

    def get_type(self, obj):
        return TRANSACTION_TYPE(obj.type).label

    class Meta:
        model = Transaction
        fields = [ "id", "payment_date", "status", "type", "amount" ]