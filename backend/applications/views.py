from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from applications.serializers import ApplicationSerializer
from applications.models import Application
from users.permissions import IsLandLordOrTenant, IsManager

class ApplicationView(viewsets.ModelViewSet):
    queryset =  Application.objects.all()
    serializer_class =  ApplicationSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsLandLordOrTenant()]
        
        if self.action == "destroy":
            return [IsAuthenticated(), IsManager()]
        
        return [IsAuthenticated()]

