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

        self.client = APIClient()
        self.land_lord = User.objects.create(
            email="test@llord.com",
            password="123123",
            first_name="LandLord",
            last_name="Natnael",
            role=UserTypes.LANDLORD
        )
        self.listing_manager = User.objects.create(
            email="test@listing.com",
            password="123123",
            first_name="Listing",
            last_name="Natnael",
            role=UserTypes.LISTING_MANAGER
        )

        self.general_manager = User.objects.create(
            email="test@general.com",
            password="123123",
            first_name="general",
            last_name="Kidus",
            role=UserTypes.GENERAL_MANAGER
        )

        self.property = Property.objects.create(
            owner=self.land_lord,
            availability=["2020-10-10T12:00:00Z"],
            category=[1, 2, 3],
            latitude=38.8941,
            longitude=-77.0364,
            facilities=["Kitchen"]
        )

        self.token_general_manager = Token.objects.create(
            user=self.general_manager)
        self.token_landlord = Token.objects.create(user=self.land_lord)
        self.token_listing_manager = Token.objects.create(
            user=self.listing_manager)

    def test_create_property_by_general_manager_should_fail(self):
        data = {
            "owner": self.general_manager.id,
            "availability": ["2020-10-10T12:00:00Z"],
            "category": [1, 2, 3],
            "latitude": 131,
            "longitude": 121
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
        response = self.client.post("/api/v1/properties/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_property_by_land_lord_should_pass(self):
        data = {
            "owner": self.land_lord.id,
            "availability": ["2020-10-10T12:00:00Z"],
            "category": [1, 2, 3],
            "latitude": 121,
            "longitude": 121
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
        response = self.client.post("/api/v1/properties/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_property_by_listing_manager_should_pass(self):
        data = {
            "owner": self.land_lord.id,
            "availability": ["2020-10-10T12:00:00Z"],
            "category": [1, 2, 3],
            "latitude": 121,    
            "longitude": 131
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_listing_manager.key)
        response = self.client.post("/api/v1/properties/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_property_details_by_id(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
        response = self.client.get(f"/api/v1/properties/{self.property.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users(self):
        response = self.client.get("/api/v1/properties/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_partial_update_property_detail(self):
        id = self.property.id
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
        response = self.client.patch(
            f"/api/v1/properties/{id}/", {"latitude": 756}, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_update_property_detail(self):
        id = self.property.id
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_listing_manager.key)

        response = self.client.put(f"/api/v1/properties/{id}/", {
            "availability": [
                "2020-10-10T12:00:00Z"
            ],
            "category": [
                1,
                2,
                3
            ],
            "latitude": "123.000000",
            "longitude": "123.000000",
            "facilities": [
                "Bathroom"
            ],
            "owner": self.land_lord.id,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
