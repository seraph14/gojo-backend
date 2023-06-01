from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from applications.serializers import ApplicationCreateSerializer, ApplicationViewSerializer
from applications.models import Application
from applications.filters import ApplicationFilter
from applications.utilities import APPLICATION_STATUS
from users.permissions import IsLandLordOrTenant, IsLandLordOrTenant, IsTenant, UserTypes
from properties.models import Property

class ApplicationView(viewsets.ModelViewSet):
    queryset =  Application.objects.all()
    lookup_field = "pk"
    
    # Filters
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter
    
    def get_queryset(self):
        queryset = Application.objects.all()
        if self.request.user.role == UserTypes.LANDLORD:
            return queryset.filter(property__owner=self.request.user)
        if self.request.user.role == UserTypes.TENANT:
            return queryset.filter(tenant=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsTenant()]
        return [IsAuthenticated(), IsLandLordOrTenant()]

    def create(self, request):
        self.request.data["tenant"] = self.request.user.id
        self.request.data["property"] = self.request.data["property_id"]
        serializer = ApplicationCreateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"], name="withdraw_application")
    def withdraw(self, request, pk=None):
        obj = self.get_object()
        obj.status = APPLICATION_STATUS.WITHDRAWN
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == "list":
            return ApplicationViewSerializer
        return ApplicationViewSerializer