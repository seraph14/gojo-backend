from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from datetime import datetime
from properties.models import Property
from users.models import User
from users.utilities import UserTypes


class UserViewsTest(APITestCase):
    def setUp(self):
        from properties.models import Category
        from properties.models import Facility

        self.facility_1 = Facility.objects.create(name="Bedroom")
        self.facility_2 = Facility.objects.create(name="Bathroom")
        self.facility_3 = Facility.objects.create(name="Square area")

        self.apartment = Category.objects.create(name="Apartment")
        self.studio = Category.objects.create(name="Studio")
        self.vila = Category.objects.create(name="Vila")
        self.condo = Category.objects.create(name="Condo")
        self.office = Category.objects.create(name="Office")
        self.warehouse = Category.objects.create(name="Warehouse")
        self.client = APIClient()
        self.land_lord = User.objects.create_user(
            email="test@llord.com",
            phone="0955211643",
            password="123123",
            first_name="LandLord",
            last_name="Natnael",
            role=UserTypes.LANDLORD,
            is_active=True,
        )
        self.listing_manager = User.objects.create_user(
            phone="0955211642",
            email="test@listing.com",
            password="123123",
            first_name="Listing",
            last_name="Natnael",
            is_active=True,
            role=UserTypes.LISTING_MANAGER,
        )

        self.general_manager = User.objects.create_user(
            is_active=True,
            phone="0955211644",
            email="test@general.com",
            password="123123",
            first_name="general",
            last_name="Kidus",
            role=UserTypes.GENERAL_MANAGER,
        )

        self.property = Property.objects.create(
            owner=self.land_lord,
            visiting_hours=[
                {"day": "Monday", "from": "9:00 AM", "to": "11:00 AM"},
            ],
            category=self.condo,
            title="TEST TITle",
            description="description",
            start_date="2020-10-10",
            amount=500
        )

        self.token_general_manager = Token.objects.create(user=self.general_manager)
        self.token_landlord = Token.objects.create(user=self.land_lord)
        self.token_listing_manager = Token.objects.create(user=self.listing_manager)

    def test_get_property_details_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_landlord.key)
        response = self.client.get(f"/api/v1/properties/{self.property.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_property_transactions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_landlord.key)
        from users.models import AccountBalance

        AccountBalance.objects.create(user=self.land_lord)

        response = self.client.get(f"/api/v1/transactions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
