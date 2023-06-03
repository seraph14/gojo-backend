from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from applications.serializers import ApplicationCreateSerializer, ApplicationViewSerializer, ContractSerializer
from applications.models import Application, Contract
from applications.filters import ApplicationFilter
from applications.utilities import APPLICATION_STATUS
from users.permissions import IsLandLordOrTenant, IsLandLordOrTenant, IsTenant, UserTypes
from properties.models import Property
from transactions.models import UserRentedProperties
from appointments.models import Appointment
from backend.utilities import application_approved
class ApplicationView(viewsets.ModelViewSet):
    queryset =  Application.objects.all()
    lookup_field = "pk"
    
    # Filters
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApplicationFilter
    

    def get_queryset(self):
        queryset = Application.objects.all()
        if self.request.user.role == UserTypes.LANDLORD:
            queryset = queryset.filter(property__owner=self.request.user)
        if self.request.user.role == UserTypes.TENANT:
            queryset = queryset.filter(tenant=self.request.user)

        property_id = self.request.query_params.get("propertyId", None)
        if property_id:
            queryset = queryset.filter(property__id=int(property_id))

        return queryset

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsTenant()]
        return [IsAuthenticated(), IsLandLordOrTenant()]

    def create(self, request):
        self.request.data["tenant"] = self.request.user.id
        self.request.data["property"] = self.request.data["property_id"]
        application = Application.objects.filter(
            property__id=self.request.data["property_id"], tenant=self.request.user
        )
        if application.exists():
            self.request.data["status"] = APPLICATION_STATUS.PENDING
            serializer = ApplicationCreateSerializer(application.first(), data=self.request.data)
        else: 
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

    @action(detail=True, methods=["DELETE"], name="withdraw_application")
    def applications(self, request, pk=None):
        obj = self.get_object()
        obj.status = APPLICATION_STATUS.WITHDRAWN
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == "list":
            return ApplicationViewSerializer
        return ApplicationViewSerializer
    
    @action(detail=True, methods=["POST"], name="approve_application")
    def approve(self, request, pk=None):
        application = self.get_object()
        application.status = APPLICATION_STATUS.APPROVED
        application.save()
        tenant = application.tenant
        UserRentedProperties.objects.create(
            property=application.property,
            user=application.tenant,
            start_date=application.possible_start_date,
        )
        self.request.data["start_date"] = application.possible_start_date
        self.request.data["property"] = application.property.pk
        self.request.data["user"] = self.request.user.pk

        serializer = ContractSerializer(data= self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            application_approved(application.tenant)
        except:
            pass
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)