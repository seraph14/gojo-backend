from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from properties.serializers import (
    PropertyCreateSerializer,
    PropertySerializer,
    CategorySerializer,
    FacilitySerializer,
    PropertySerializerForProfile,
    VirtualTourSerializer
)
from properties.models import Property, Category, Facility, VirtualTour
from users.permissions import (
    IsLandlord,
    IsManager,
    CanEditPropertyDetail,
    CanCreateProperty
)
from users.serializers import BasicUserSerializer

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"
    # permission_classes = [IsManager]
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
        if self.action == "favorites" or self.action == "rented":
            return PropertySerializerForProfile

        return PropertySerializer

    @action(detail=False, methods=["GET", "POST"], name="favorite_properties")
    def favorites(self, request):
        if self.request.method == "POST":
            pass
        '''
        serializer:
            PropertyItem(
                id: "1",
                title: "Villa, Kemah Tinggi",
                thumbnailUrl: Resources.gojoImages.sofaNetwork,
                category: "Villa",
                facilities: [
                    Facility(name: "Kitchen", count: 1),
                    Facility(name: "Bedroom", count: 2),
                ],
                rent: 14000,
                rating: 4.9,
            ),        
        '''
        # TODO: do the necessary querying
        return super().list(request)

    @action(detail=False, methods=["GET"], name="rented_properties")
    def rented(self, request):
        '''
        serializer:
            PropertyItem(
                id: "1",
                title: "Villa, Kemah Tinggi",
                thumbnailUrl: Resources.gojoImages.sofaNetwork,
                category: "Villa",
                facilities: [
                    Facility(name: "Kitchen", count: 1),
                    Facility(name: "Bedroom", count: 2),
                ],
                rent: 14000,
                rating: 4.9,
            ),        
        '''
        # TODO: do the necessary querying
        return super().list(request)


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
            virtual_tour = create_virtual_tour_object(data, imgs, self.get_object())
            return Response(VirtualTourSerializer(virtual_tour).data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)


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


