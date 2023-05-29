from rest_framework import serializers
from properties.models import Property, PropertyImage, Category, Facility, PropertyFacility, PropertyLocation
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

class PropertyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyLocation
        fields = ["name", "longitude", "latitude"]

# TODO: For Editing property replace this serializer
class PropertyFacilitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="facility.name")
    count = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
    
    class Meta:
        model = PropertyFacility
        fields = [ "name", "count" ]

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    owner = UserSerializer()
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    facilities = PropertyFacilitySerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        # TODO: replace with a valid rating
        return 4.5

    def get_category(self, obj):    
        return obj.category.name

    def get_thumbnail_url(self, obj):
        # TODO: replace this thumbnail url
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTooc7RcJtAj9LLZyHrnxkx_jlzFmT12YAy6bLt3eYRLnoYXV_cqSBg1SUcPDRq8fHzXKI&usqp=CAU"
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
            facility_id, *amount = facility_data
            facility = Facility.objects.get(id=facility_id)
            if amount:
                amount = amount[0]
                PropertyFacility.objects.create(property=property, facility=facility, amount=amount)
            else:
                PropertyFacility.objects.create(property=property, facility=facility)
        
        return property


class BasicPropertySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    def get_thumbnail_url(self, obj):
        return "https://shared-s3.property.ca/public/images/listings/optimized/c5985711/mls/c5985711_1.jpg?v=2"

    def get_category(self, obj):    
        return obj.category.name
   
    class Meta:
        model = Property
        fields = ["id", "title", "category", "amount", "thumbnail_url"]
        read_only_fields = ("id",)

class PropertySerializerForProfile(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    facilities = PropertyFacilitySerializer(many=True)
    rating = serializers.SerializerMethodField()


    # FIXME: on the model replace the location json field b/c longitude and latitude are decimal
    


    def get_thumbnail_url(self, obj):
        return "https://shared-s3.property.ca/public/images/listings/optimized/c5985711/mls/c5985711_1.jpg?v=2"

    def get_category(self, obj):    
        return obj.category.name
    
    def get_rating(self, obj):
        # TODO: replace with a valid rating
        return 4.5
    
    class Meta:
        model = Property
        fields = ["id", "title", "category", "amount", "facilities", "rating", "thumbnail_url"]
        read_only_fields = ("id",)