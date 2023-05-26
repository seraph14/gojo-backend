from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from properties.serializers import PropertyCreateSerializer, PropertySerializer, CategorySerializer, FacilitySerializer
from properties.models import Property, Category, Facility
from users.permissions import IsLandlord, IsManager, CanEditPropertyDetail, CanCreateProperty


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"
    permission_classes = [IsManager]

class FacilityView(viewsets.ModelViewSet):
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()
    lookup_field = "pk"
    permission_classes = [IsManager]

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
        return PropertySerializer
