import os
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser
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
    VirtualTour,
    # this is for favorites
    Favorites,
)
from users.serializers import UserSerializer
from users.models import User
from users.serializers import UserSerializer, BasicUserSerializer
from reviews.serializers import ReviewSerializer
from reviews.models import Review
from properties.utils import calculate_rating
from chat.models import Thread
from chat.serializers import ThreadSerializer
from applications.models import Contract


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = "__all__"


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
        fields = ["street", "longitude", "latitude"]


class PropertyLocationViewSerializer(serializers.ModelSerializer):
    longitude = serializers.DecimalField(
        max_digits=30, decimal_places=15, coerce_to_string=False
    )
    latitude = serializers.DecimalField(
        max_digits=30, decimal_places=15, coerce_to_string=False
    )

    class Meta:
        model = PropertyLocation
        fields = ["street", "longitude", "latitude"]


# TODO: For Editing property replace this serializer
class PropertyFacilitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="facility.name")
    amount = serializers.DecimalField(
        max_digits=30,
        decimal_places=15,
        coerce_to_string=False,
        source="count",
        allow_null=True,
    )

    class Meta:
        model = PropertyFacility
        fields = ["name", "amount", "id"]


class PropertySerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    images = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    facilities = PropertyFacilitySerializer(many=True)
    rating = serializers.SerializerMethodField()
    location = PropertyLocationViewSerializer()
    reviews = ReviewSerializer(many=True)
    favorite = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    amount = serializers.DecimalField(
        max_digits=30,
        decimal_places=2,
    )

    def get_messages(self, obj):
        request = self.context["request"]
        if request.user.is_authenticated:
            thread = Thread.objects.filter(tenant=request.user, landlord=obj.owner)
            if thread.exists():
                serializer = ThreadSerializer(thread.first(), context=self.context)
                return serializer.data["messages"]
        return []

    def get_favorite(self, obj):
        if self.context["request"].user.is_authenticated:
            return Favorites.objects.filter(
                property=obj, user=self.context["request"].user
            ).exists()
        return True

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        return calculate_rating(reviews)

    def get_category(self, obj):
        return obj.category.name

    def get_images(self, obj):
        image_serializer = PropertyImageSerializer(
            obj.images.all(), many=True, context=self.context
        )
        return [image["image"] for image in image_serializer.data]

    def get_thumbnail_url(self, obj):
        if not obj.images.exists():
            return "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80"

        image_data = PropertyImageSerializer(obj.images.first(), context=self.context)
        if len(image_data.data) != 0:
            if str(image_data.data["image"]).startswith("http"):
                return str(image_data.data["image"])
            return str(os.environ.get("DOMAIN", "http://localhost:8000")) + str(
                image_data.data["image"]
            )

    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("id",)


class PropertyUpdateAdminSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        data = {"property": instance.id}
        for key, value in self.context["request"].data.items():
            if key.startswith("image"):
                data["image"] = self.context["request"].data[key]
                serializer = PropertyImageSerializer(data=data, context=self.context)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Property
        fields = "__all__"


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
        # images_data = validated_data.pop('images', [])

        address = self.context["request"].data["address"]

        category_data = self.context["request"].data["category"]

        category_instance = Category.objects.get(id=category_data["id"])

        property_instance = Property.objects.create(
            owner=owner, category=category_instance, **validated_data
        )

        facilities = []
        property_facility = self.context["request"].data["facilities"]
        for facility in property_facility:
            facility_instance = Facility.objects.get(id=facility["id"])
            if facility["amount"] == None:
                facilities.append(
                    PropertyFacility.objects.get_or_create(
                        property=property_instance,
                        facility=facility_instance,
                        count=0,
                    )
                )
            else:
                facilities.append(
                    PropertyFacility.objects.get_or_create(
                        property=property_instance,
                        facility=facility_instance,
                        count=facility["amount"],
                    )
                )
        address_instance, _ = PropertyLocation.objects.get_or_create(
            property=property_instance, **address
        )

        return property_instance

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", [])
        instance = super().update(instance, validated_data)

        for image_data in images_data:
            PropertyImage.objects.create(property=instance, image=image_data)

        return instance


class BasicPropertySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    def get_thumbnail_url(self, obj):
        if not obj.images.exists():
            return "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80"

        image_data = PropertyImageSerializer(obj.images.first(), context=self.context)
        if len(image_data.data) != 0:
            if str(image_data.data["image"]).startswith("http"):
                return str(image_data.data["image"])
            return str(os.environ.get("DOMAIN", "http://localhost:8000")) + str(
                image_data.data["image"]
            )

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Property
        fields = ["id", "title", "category", "amount", "thumbnail_url", "status"]
        read_only_fields = ("id",)


class PropertySerializerForProfile(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    facilities = PropertyFacilitySerializer(many=True)
    rating = serializers.SerializerMethodField()
    contract_url = serializers.SerializerMethodField()
    address = PropertyLocationSerializer(source="location")
    amount = serializers.DecimalField(max_digits=30, decimal_places=2)

    def get_contract_url(self, obj):
        contract = Contract.objects.filter(
            application__property__id=obj.id,
            application__tenant__id=self.context["request"].user.id,
        )
        if contract.exists():
            contract = contract.latest()
            if contract:
                return str(os.environ.get("DOMAIN", "http://localhost:8000")) + str(
                    contract.contract.url
                )
        return None

    def get_thumbnail_url(self, obj):
        if not obj.images.exists():
            return "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80"

        image_data = PropertyImageSerializer(obj.images.first(), context=self.context)

        if image_data.data.get("image", None) and len(image_data.data) != 0:
            if str(image_data.data["image"]).startswith("http"):
                return str(image_data.data["image"])
            return str(os.environ.get("DOMAIN", "http://localhost:8000")) + str(
                image_data.data["image"]
            )

        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTooc7RcJtAj9LLZyHrnxkx_jlzFmT12YAy6bLt3eYRLnoYXV_cqSBg1SUcPDRq8fHzXKI&usqp=CAU"

    def get_category(self, obj):
        return obj.category.name

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        return calculate_rating(reviews)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "category",
            "amount",
            "facilities",
            "rating",
            "thumbnail_url",
            "description",
            "status",
            "contract_url",
            "address",
        ]
        read_only_fields = ("id",)


############### Marker Serializer #################
class MarkerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    latitude = serializers.DecimalField(
        max_digits=30, decimal_places=20, coerce_to_string=False
    )
    longitude = serializers.DecimalField(
        max_digits=30, decimal_places=20, coerce_to_string=False
    )

    def get_image(self, obj):
        import os

        return (
            os.environ.get(
                "DOMAIN",
                "http://localhost:8000",
            )
            + "panorama_images/marker.png"
        )

    class Meta:
        model = Marker
        fields = "__all__"


############### Link Serializer #################
class LinkSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(
        max_digits=30, decimal_places=20, coerce_to_string=False
    )
    longitude = serializers.DecimalField(
        max_digits=30, decimal_places=20, coerce_to_string=False
    )

    class Meta:
        model = Link
        fields = "__all__"


############### HotspotNode Serializer #################


class HotspotNodeSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True)
    markers = MarkerSerializer(many=True)
    panorama = serializers.SerializerMethodField()

    def get_panorama(self, obj):
        import os

        return os.environ.get("DOMAIN", "http://localhost:8000") + obj.panorama.url

    class Meta:
        model = HotspotNode
        fields = "__all__"


############### Marker Serializer #################
class VirtualTourSerializer(serializers.ModelSerializer):
    defaultViewPosition = serializers.SerializerMethodField()
    hotspotNodes = HotspotNodeSerializer(many=True)

    def get_defaultViewPosition(self, obj):
        from decimal import Decimal

        return {
            "latitude": (obj.defaultViewPosition_latitude),
            "longitude": (obj.defaultViewPosition_longitude),
        }

    def create(self, validated_data):
        import json
        from decimal import Decimal
        from properties.models import Link, Marker, HotspotNode, VirtualTour

        default_view_position = validated_data.pop("defaultViewPosition")
        virtual_tour = VirtualTour.objects.create(
            property=property,
            defaultViewPosition_latitude=Decimal(default_view_position.get("latitude")),
            defaultViewPosition_longitude=Decimal(
                default_view_position.get("longitude")
            ),
            initialView=data.get("initialView", None),
        )

        nodes = []
        hotspot_nodes = validated_data.pop("hotspotNodes")

        for node in hotspot_nodes:
            hotspot_node = HotspotNode.objects.create(
                id=node.get("id"),
                panorama=data[node.get("id")],
                virtual_tour=virtual_tour,
            )

            links = []
            for link in node.get("links", []):
                _link = Link.objects.create(
                    nodeId=link.get("nodeId"),
                    latitude=Decimal(link.get("latitude")),
                    longitude=Decimal(link.get("longitude")),
                    node=hotspot_node,
                )

                links.append(_link)

            hotspot_node.links.set(links)

            markers = []
            for marker in node.get("markers", []):
                _marker = Marker.objects.create(
                    id=marker.get("id", ""),
                    linksTo=marker.get("linksTo"),
                    tooltip=marker.get("tooltip", ""),
                    width=marker.get("width"),
                    height=marker.get("height"),
                    longitude=Decimal(marker.get("longitude")),
                    latitude=Decimal(marker.get("longitude")),
                    anchor=marker.get("anchor"),
                    node=hotspot_node,
                )

                markers.append(_marker)

            hotspot_node.markers.set(markers)

            nodes.append(hotspot_node)

        virtual_tour.hotspotNodes.set(nodes)

        return virtual_tour

    class Meta:
        model = VirtualTour
        fields = "__all__"


class PropertyUpdateSerializer(serializers.ModelSerializer):
    facilities = PropertyFacilitySerializer(many=True)
    category = CategorySerializer()
    address = PropertyLocationSerializer(source="location")

    def update(self, instance, validated_data):
        owner = self.context["request"].user

        validated_data.pop("facilities")
        validated_data.pop("category")
        validated_data.pop("location")

        address = self.context["request"].data["address"]

        category_data = self.context["request"].data["category"]

        category_instance = Category.objects.get(id=category_data["id"])

        property_instance = Property.objects.get(id=self.context["request"].data["id"])
        property_instance.title = validated_data["title"]
        property_instance.category = category_instance
        property_instance.description = validated_data["description"]
        property_instance.amount = validated_data["amount"]
        property_instance.save()
        # property_instance, created = Property.objects.update_or_create(
        #     owner=owner,
        #     category=category_instance,
        #     **validated_data,
        #     defaults={"id": int(self.context["request"].data["id"])}
        # )

        facilities = []
        property_facility = self.context["request"].data["facilities"]
        for facility in property_facility:
            facility_instance = Facility.objects.get(id=facility["id"])
            if facility["amount"] == None:
                d = PropertyFacility.objects.get(
                    property=property_instance, facility=facility_instance
                )
                d.amount = 0
                d.save()
            else:
                d = PropertyFacility.objects.get(
                    property=property_instance, facility=facility_instance
                )
                if facility["name"]  != "Square area": 
                    d.amount = int(facility["amount"])
                else:
                    d.amount = facility["amount"]
                d.save()

        location= PropertyLocation.objects.get(
            property=property_instance
        )

        location.street = address["street"]
        location.latitude = address["latitude"]
        location.longitude = address["longitude"]
        location.save()

        return property_instance

    class Meta:
        model = Property
        fields = "__all__"
