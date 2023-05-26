from rest_framework import serializers
from properties.models import Property, PropertyImage, Category, Facility, PropertyFacility
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

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"

class PropertyFacilitySerializer(serializers.ModelSerializer):
    facility = FacilitySerializer()
    class Meta:
        model = PropertyFacility
        fields = [ "facility" ]

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    owner = UserSerializer()
    categories = CategorySerializer(many=True, required=False)
    facilities = PropertyFacilitySerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id",)


class PropertyCreateSerializer(serializers.ModelSerializer):
    facilities = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField()))
    categories = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Property
        fields = "__all__"

    def create(self, validated_data):
        facilities_data = validated_data.pop('facilities')
        categories_data = validated_data.pop('categories')
        property = Property.objects.create(**validated_data)

        property.categories.set(Category.objects.filter(id__in=categories_data))

        for facility_data in facilities_data:
            print("============================== ", facility_data)
            facility_id, *amount = facility_data
            print("==============================")
            facility = Facility.objects.get(id=facility_id)
            if amount:
                amount = amount[0]
                PropertyFacility.objects.create(property=property, facility=facility, amount=amount)
            else:
                PropertyFacility.objects.create(property=property, facility=facility)
        
        print("=================DONE________________")
        return property