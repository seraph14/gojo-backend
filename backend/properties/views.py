from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import AnonymousUser
from properties.serializers import (
    PropertyCreateSerializer,
    PropertySerializer,
    CategorySerializer,
    FacilitySerializer,
    PropertySerializerForProfile,
    VirtualTourSerializer
)
from properties.models import (
    Property,
    Category,
    Facility,
    VirtualTour,
    Favorites,
)
from transactions.models import UserRentedProperties

from users.permissions import (
    UserTypes,
    IsLandlord,
    IsManager,
    CanEditPropertyDetail,
    CanCreateProperty
)
from users.serializers import BasicUserSerializer
from reviews.serializers import ReviewSerializer
from reviews.models import Review

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"
    permission_classes = [AllowAny]


class FacilityView(viewsets.ModelViewSet):
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()
    lookup_field = "pk"
    # permission_classes = [IsManager]
    permission_classes = [AllowAny]


class PropertyView(
    viewsets.ModelViewSet
):
    queryset = Property.objects.all().prefetch_related('images')
    lookup_field = "pk"

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve":
            return [AllowAny()]

        if self.action == "create":
            return [IsAuthenticated(), CanCreateProperty()]

        if self.action == "partial_update" or self.action == "update" or self.action == "create":
            return [IsAuthenticated(), CanEditPropertyDetail()]

        if self.action == "destroy":
            return [IsAuthenticated(), IsManager()]

        return [AllowAny()]

    def perform_create(self, serializer):
        instance = serializer.save()
        property_serializer = PropertySerializer(instance)
        self.request._property_data = property_serializer.data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if hasattr(self.request, '_property_data'):
            data = self.request._property_data
            del self.request._property_data
        return Response(data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PropertyCreateSerializer

        if type(self.request.user) != AnonymousUser and self.request.user.role not in [UserTypes.LISTING_MANAGER, UserTypes.GENERAL_MANAGER]:
            self.queryset = Property.objects.filter(is_approved=True)

        if self.action == "favorites" or self.action == "rented":
            return PropertySerializerForProfile

        return PropertySerializer

    @action(detail=True, methods=["PATCH"], name="favorite_properties")
    def favorite(self, request, pk=None):
        try:
            Favorites.objects.get(user=self.request.user, property=self.get_object()).delete()
            return Response({"message": "removed from favorites"}, status=status.HTTP_200_OK)
        except Favorites.DoesNotExist:
            Favorites.objects.create(
                user=self.request.user,
                property=self.get_object()
            )
            return Response({"message": "saved to favorites"}, status=status.HTTP_200_OK)
            
    @action(detail=False, methods=["GET"], name="rented_properties")
    def rented(self, request):
        from transactions.models import PROPERTY_RENT_STATUS
        data = []

        for rent in UserRentedProperties.objects.filter(user=self.request.user):
            data.append(rent)

        return Response(self.get_serializer(data, many=True).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET", "POST"], name="virtual_tour")
    def virtual_tour(self, request, pk=None):
        if self.request.method == "GET":
            return Response(VirtualTourSerializer(VirtualTour.objects.get(property=self.get_object())).data, status=status.HTTP_200_OK)

        objects = VirtualTour.objects.filter(property=self.get_object())
        if self.request.method == "POST":
            import json
            from properties.utils import create_virtual_tour_object
            data = json.loads(self.request.POST["data"])
            imgs = self.request.POST
            if VirtualTour.objects.filter(property=self.get_object()).exists():
                return Response({"message" : "Has a virtual tour!"}, status=status.HTTP_400_BAD_REQUEST)
            virtual_tour = create_virtual_tour_object(
                data, imgs, self.get_object())
            return Response(VirtualTourSerializer(virtual_tour).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET", "POST"], name="virtual_tour")
    def review(self, request, pk=None):
        return Response(ReviewSerializer(Review.objects.create(
            user=self.request.user,
            rating=self.request.data["rating"],
            comment=self.request.data["comment"],
            property=self.get_object()
        )).data, status=status.HTTP_200_OK)


# TODO: Property Appointment
# TODO: 1. schedule appointment
# The appointment data is going to be like this:
'''
AvailabilityModel(
        days: [1, 2, 3, 4, 5],
        timeSlots: {
          "1": ["10:00 AM", "11:00 AM", "12:00 AM"],
          "2": ["10:00 AM", "11:00 AM", "12:00 AM"],
          "3": ["9:00 AM", "11:00 AM", "12:00 AM"],
        },
      )
'''
# TODO: 1. cancel appointment
