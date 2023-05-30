from rest_framework import serializers
from properties.models import (
    Property, 
    PropertyImage, 
    Category, 
    Facility, 
    PropertyFacility, 
    PropertyLocation,
    Marker,
    Link,
    HotspotNode,
    VirtualTour
)
from users.serializers import UserSerializer
from users.models import User
from users.serializers import UserSerializer, BasicUserSerializer
from reviews.serializers import ReviewSerializer


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
    amount = serializers.DecimalField(max_digits=30, decimal_places=15, coerce_to_string=False, source="count")
    
    class Meta:
        model = PropertyFacility
        fields = [ "name", "amount" , "id"]

class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, required=False)
    owner = UserSerializer()
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    facilities = PropertyFacilitySerializer(many=True)
    rating = serializers.SerializerMethodField()
    location = PropertyLocationSerializer()
    reviews = ReviewSerializer(many=True)

    def get_rating(self, obj):
        # TODO: replace with a valid rating
        return 4.5

    def get_category(self, obj):    
        return obj.category.name

    def get_thumbnail_url(self, obj):
        imgs = obj.images
        if imgs.count() != 0:
            return imgs[0]
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTooc7RcJtAj9LLZyHrnxkx_jlzFmT12YAy6bLt3eYRLnoYXV_cqSBg1SUcPDRq8fHzXKI&usqp=CAU"
   
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id",)


class PropertyCreateSerializer(serializers.ModelSerializer):
    facilities = PropertyFacilitySerializer(many=True)
    category = CategorySerializer()
    address = PropertyLocationSerializer(source="location")
    owner = BasicUserSerializer(read_only=True)
    images = serializers.ListField(child=serializers.ImageField(), required=False)

    class Meta:
        model = Property
        fields = "__all__"

    def create(self, validated_data):
        owner = self.context["request"].user

        validated_data.pop("facilities")
        validated_data.pop("category")
        validated_data.pop("location")
        images_data = validated_data.pop('images', [])

        address = self.context["request"].data["address"]

        category_data = self.context["request"].data["category"]

        category_instance = Category.objects.get(id=category_data["id"])
    
        property_instance = Property.objects.create(owner=owner, category=category_instance, **validated_data)

        facilities = []
        property_facility = self.context["request"].data["facilities"]
        for facility in property_facility:
            facility_instance = Facility.objects.get(id=facility["id"])
            facilities.append(PropertyFacility.objects.get_or_create(
                property=property_instance,
                facility=facility_instance, 
                count=facility["amount"] # FIXME:the naming is not consistent
            ))

        address_instance, _ = PropertyLocation.objects.get_or_create(property=property_instance, **address)

        for image in images_data:
            image = PropertyImage.objects.create(property=property_instance, image=image)

        return property_instance

    # def create(self, validated_data):
    #     facilities_data = validated_data.pop('facilities')
    #     categories_data = validated_data.pop('categories')
    #     property = Property.objects.create(**validated_data)

    #     property.categories.set(Category.objects.filter(id__in=categories_data))

    #     for facility_data in facilities_data:
    #         facility_id, *amount = facility_data
    #         facility = Facility.objects.get(id=facility_id)
    #         if amount:
    #             amount = amount[0]
    #             PropertyFacility.objects.create(property=property, facility=facility, amount=amount)
    #         else:
    #             PropertyFacility.objects.create(property=property, facility=facility)
        
    #     return property


class BasicPropertySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    def get_thumbnail_url(self, obj):
        imgs = obj.images
        if imgs.count() != 0:
            return imgs[0]
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTooc7RcJtAj9LLZyHrnxkx_jlzFmT12YAy6bLt3eYRLnoYXV_cqSBg1SUcPDRq8fHzXKI&usqp=CAU"
   
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


    def get_thumbnail_url(self, obj):
        imgs = obj.images
        if imgs.count() != 0:
            return imgs[0]
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTooc7RcJtAj9LLZyHrnxkx_jlzFmT12YAy6bLt3eYRLnoYXV_cqSBg1SUcPDRq8fHzXKI&usqp=CAU"
   
    def get_category(self, obj):    
        return obj.category.name
    
    def get_rating(self, obj):
        # TODO: replace with a valid rating
        return 4.5
    
    class Meta:
        model = Property
        fields = ["id", "title", "category", "amount", "facilities", "rating", "thumbnail_url"]
        read_only_fields = ("id",)


############### Marker Serializer #################
class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = "__all__"

############### Link Serializer #################
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"

############### HotspotNode Serializer #################
class HotspotNodeSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True)
    markers = MarkerSerializer(many=True)

    class Meta:
        model = HotspotNode
        fields = "__all__"


############### Marker Serializer #################
class VirtualTourSerializer(serializers.ModelSerializer):
    defaultViewPosition = serializers.SerializerMethodField()
    hotspotNodes = HotspotNodeSerializer(many=True)

    def get_defaultViewPosition(self, obj):
        return {
            "latitude": obj.defaultViewPosition_latitude, 
            "longitude": obj.defaultViewPosition_latitude 
        }

    class Meta:
        model = VirtualTour
        fields = "__all__"
