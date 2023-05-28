from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from applications.serializers import ApplicationCreateSerializer, ApplicationViewSerializer
from applications.models import Application
from applications.filters import ApplicationFilter
from users.permissions import IsLandLordOrTenant, IsLandLordOrTenant, IsTenant

class ApplicationView(viewsets.ModelViewSet):
    queryset =  Application.objects.all()
    lookup_field = "pk"
    
    # Filters
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsTenant()]

        return [IsAuthenticated(), IsLandLordOrTenant()]

    def get_serializer_class(self):
        if self.action == "list":
            return ApplicationViewSerializer
        return ApplicationCreateSerializer