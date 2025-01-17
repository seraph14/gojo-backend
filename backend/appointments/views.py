from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from appointments.serializers import (
    AppointmentCreateSerializer,
    AppointmentViewSerializer,
)
from appointments.models import Appointment
from appointments.filters import AppointmentFilter
from appointments.utils import APPOINTMENT_STATUS
from users.permissions import (
    IsLandLordOrTenant,
    IsLandLordOrTenant,
    IsTenant,
    UserTypes,
)
from django.contrib.auth.models import AnonymousUser
from backend.utilities import appointment_approved


class AppointmentView(viewsets.ModelViewSet):
    lookup_field = "pk"
    queryset = Appointment.objects.exclude(
        status__in=[APPOINTMENT_STATUS.CANCELED, APPOINTMENT_STATUS.REJECTED]
    )

    # Filters
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentFilter

    # def get_permissions(self):
    #     if self.action == "create":
    #         return [IsAuthenticated(), IsTenant()]
    #     return [IsAuthenticated(), IsLandLordOrTenant()]
    def get_queryset(self):
        queryset = Appointment.objects.all()
        property_id = self.request.query_params.get("propertyId", None)
        if property_id:
            queryset = queryset.filter(property__id=int(property_id))
        return queryset

    @action(detail=True, methods=["DELETE"], name="cancel_appointment")
    def cancel(self, request, pk=None):
        obj = self.get_object()
        obj.status = APPOINTMENT_STATUS.CANCELED
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"], name="approve_appointment")
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.status = APPOINTMENT_STATUS.APPROVED
        obj.save()
        appointment_approved(
            obj.tenant.fb_registration_token, obj.property.title, obj.appointment_date
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == "list":
            user = self.request.user
            if type(user) != AnonymousUser and user.role in [
                UserTypes.TENANT,
                UserTypes.LANDLORD,
            ]:
                self.queryset = self.queryset.filter(tenant=user)

            return AppointmentViewSerializer
        return AppointmentViewSerializer
