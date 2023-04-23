from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from properties.serializers import PropertySerializer
from properties.models import Property
from users.permissions import IsLandlord, IsManager, CanEditPropertyDetail


class PropertyView(
    viewsets.ModelViewSet
):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    lookup_field = "pk"

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve":
            return [AllowAny()]

        if self.action == "create":
            return [IsAuthenticated(), IsLandlord()]

        if self.action == "partial_update" or self.action == "update":
            return [IsAuthenticated(), CanEditPropertyDetail()]

        if self.action == "destroy":
            return [IsAuthenticated(), IsManager()]
        
        return [AllowAny()]