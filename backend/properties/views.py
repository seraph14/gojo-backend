import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import AnonymousUser
from properties.serializers import (
    PropertyCreateSerializer,
    PropertySerializer,
    CategorySerializer,
    FacilitySerializer,
    PropertySerializerForProfile,
    VirtualTourSerializer,
    PropertyUpdateAdminSerializer,
)
from properties.models import (
    Property,
    Category,
    Facility,
    VirtualTour,
    Favorites,
    PROPERTY_STATUS,
)
from transactions.models import UserRentedProperties, PROPERTY_RENT_STATUS
from appointments.models import Appointment
from appointments.serializers import AppointmentCreateSerializer


from users.permissions import (
    UserTypes,
    IsLandlord,
    IsManager,
    CanEditPropertyDetail,
    CanCreateProperty,
)
from users.serializers import BasicUserSerializer
from reviews.serializers import ReviewSerializer
from reviews.models import Review
from properties.filters import PropertyFilter
from transactions.models import PROPERTY_RENT_STATUS


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "pk"
    permission_classes = [AllowAny]


class FacilityView(viewsets.ModelViewSet):
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()
    lookup_field = "pk"
    permission_classes = [AllowAny]


class PropertyView(viewsets.ModelViewSet):
    queryset = Property.objects.all().prefetch_related("images")
    lookup_field = "pk"

    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter

    def get_permissions(self):
        if self.action == "virtual_tour":
            return [AllowAny()]

        if self.action == "list" or self.action == "retrieve":
            return [AllowAny()]

        if self.action == "create":
            return [IsAuthenticated(), CanCreateProperty()]

        if (
            self.action == "partial_update"
            or self.action == "update"
            or self.action == "create"
        ):
            return [IsAuthenticated(), CanEditPropertyDetail()]

        if self.action == "destroy":
            return [IsAuthenticated(), IsManager()]

        return [AllowAny()]

    def perform_create(self, serializer):
        instance = serializer.save()

    def get_queryset(self):
        queryset = Property.objects.all()
        if not self.request.user.is_authenticated or (
            self.request.user.is_authenticated
            and self.request.user.role == UserTypes.TENANT
        ):
            queryset = Property.objects.exclude(
                status__in=[PROPERTY_STATUS.PENDING, PROPERTY_STATUS.REJECTED],
                # rent_histories__status=PROPERTY_RENT_STATUS.ONGOING,
            )
        return queryset

    def list(self, request):
        t = request.query_params.get("type", None)
        if (
            self.request.user.is_authenticated
            and self.request.user.role == UserTypes.LANDLORD
        ):
            data = self.get_queryset()
            if t == "rented":
                data = Property.objects.filter(
                    rent_histories__status=PROPERTY_RENT_STATUS.ONGOING
                ).distinct("id")
            elif t == "posted":
                data = (
                    Property.objects.filter(owner=self.request.user, status=PROPERTY_STATUS.APPROVED)
                    .exclude(rent_histories__status=PROPERTY_RENT_STATUS.ONGOING)
                    .distinct("id")
                )
            elif t == "in_review":
                data = Property.objects.filter(
                    owner=self.request.user, status=PROPERTY_STATUS.PENDING
                )
            return Response(
                {"results": PropertySerializerForProfile(data, many=True, context={"request": self.request}).data}
            )

        return super().list(request)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PropertyCreateSerializer

        if self.request.method == "PATCH":
            return PropertyUpdateAdminSerializer

        if self.action == "favorites" or self.action == "rented":
            return PropertySerializerForProfile

        return PropertySerializer

    @action(detail=True, methods=["POST"], name="end_contract")
    def end_contract(self, request, pk=None):
        from transactions.models import PROPERTY_RENT_STATUS, Transaction
        from transactions.utils import TRANSACTION_STATUS

        obj = self.get_object()
        data = obj.rent_histories.latest()
        data.status = PROPERTY_RENT_STATUS.ENDED
        data.save()
        transactions = Transaction.objects.filter(rent_detail=data, status=TRANSACTION_STATUS.PENDING)
        if transactions.exists():
            transactions.delete()

        return Response({"message": "Done"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], name="favorite_properties")
    def favorite(self, request, pk=None):
        if self.request.method == "GET":
            properties = self.request.user.favorites
            return Response(
                {"results": PropertySerializerForProfile(properties, many=True).data}
            )
        try:
            Favorites.objects.get(
                user=self.request.user, property=self.get_object()
            ).delete()
            return Response(
                {"message": "removed from favorites"}, status=status.HTTP_200_OK
            )
        except Favorites.DoesNotExist:
            Favorites.objects.create(user=self.request.user, property=self.get_object())
            return Response(
                {"message": "saved to favorites"}, status=status.HTTP_200_OK
            )

    @action(detail=False, methods=["GET"], name="favorite_properties")
    def favorites(self, request, pk=None):
        favorites = self.request.user.favorites.all()
        properties = []
        for property in favorites:
            properties.append(property.property)
        return Response(
            {"results": PropertySerializerForProfile(properties, many=True).data}
        )

    @action(detail=False, methods=["GET"], name="rented_properties")
    def rented(self, request):
        from transactions.models import PROPERTY_RENT_STATUS

        data = []

        for rent in UserRentedProperties.objects.filter(user=self.request.user):
            data.append(rent.property)

        return Response(
            {"results": PropertySerializerForProfile(data,many=True ,context={"request": self.request}).data},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["GET", "POST"], name="virtual_tour")
    def virtual_tour(self, request, pk=None):
        if self.request.method == "GET":
            virtual_tour = VirtualTour.objects.filter(property=self.get_object())
            if not virtual_tour.exists():
                return Response(
                    {"message": "virtual tour does not exist!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                VirtualTourSerializer(virtual_tour.first()).data,
                status=status.HTTP_200_OK,
            )

        objects = VirtualTour.objects.filter(property=self.get_object())
        if self.request.method == "POST":
            import json
            from properties.utils import create_virtual_tour_object

            data = json.loads(self.request.POST["data"])

            imgs = self.request.POST

            virtual_tour = create_virtual_tour_object(data, imgs, self.get_object())
            return Response(
                VirtualTourSerializer(virtual_tour).data, status=status.HTTP_200_OK
            )

    @action(detail=True, methods=["GET", "POST"], name="review")
    def review(self, request, pk=None):
        return Response(
            ReviewSerializer(
                Review.objects.create(
                    user=self.request.user,
                    rating=self.request.data["rating"],
                    comment=self.request.data["comment"],
                    property=self.get_object(),
                )
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], name="schedule_appointment")
    def schedule_appointment(self, request, pk=None):
        from appointments.utils import APPOINTMENT_STATUS

        self.request.data["property"] = self.get_object().pk
        self.request.data["tenant"] = self.request.user.pk
        appointment_date = datetime.datetime.strptime(
            self.request.data["appointment_date"], "%Y-%m-%d"
        )
        appointment_time = datetime.datetime.strptime(
            self.request.data["appointment_time"], "%I:%M %p"
        )
        self.request.data["appointment_date"] = appointment_date.replace(
            hour=appointment_time.hour, minute=appointment_time.minute
        ).strftime("%Y-%m-%d %H:%M")

        appointment = Appointment.objects.filter(
            property__id=self.request.data["property"], tenant=self.request.user
        )

        if appointment.exists():
            self.request.data["status"] = APPOINTMENT_STATUS.PENDING
            serializer = AppointmentCreateSerializer(
                appointment.first(), self.request.data
            )
        else:
            serializer = AppointmentCreateSerializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
