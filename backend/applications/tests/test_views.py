from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from datetime import datetime
from properties.models import Property
from users.models import User
from users.utilities import UserTypes
from applications.models import Application
from applications.utilities import APPLICATION_STATUS

class ApplicationViewsTest(APITestCase):

    applications_endpoint = "/api/v1/applications/"
    
    def setUp(self):
        self.client = APIClient()
    #     self.land_lord = User.objects.create(
    #         phone="0955211655",
    #         email="test@llord.com",
    #         password="123123",
    #         first_name="LandLord",
    #         last_name="Natnael",
    #         role=UserTypes.LANDLORD
    #     )
    #     self.tenant = User.objects.create(
    #         email="test@tenant.com",
    #         password="123123",
    #         phone="0955211652",
    #         first_name="Tenant",
    #         last_name="Natnael",
    #         role=UserTypes.TENANT
    #     )

    #     self.listing_manager = User.objects.create(
    #         email="test@listing.com",
    #         phone="0955211652",
    #         password="123123",
    #         first_name="Listing",
    #         last_name="Natnael",
    #         role=UserTypes.LISTING_MANAGER
    #     )

    #     self.general_manager = User.objects.create(
    #         phone="0955211655",
    #         email="test@general.com",
    #         password="123123",
    #         first_name="general",
    #         last_name="Kidus",
    #         role=UserTypes.GENERAL_MANAGER
    #     )

    #     self.property = Property.objects.create(
    #         owner=self.land_lord,
    #         availability=["2020-10-10T12:00:00Z"],
    #         category=[1, 2, 3],
    #         latitude=38.8941,
    #         longitude=-77.0364,
    #         facilities=["Kitchen"]
    #     )

    #     self.application = Application.objects.create(
    #         description="Some description",
    #         tenant=self.tenant,
    #         landlord=self.land_lord,
    #         status=APPLICATION_STATUS.SIGNED,
    #         property=self.property
    #     )

    #     self.test_data = {
    #         "tenant" : self.tenant.id,
    #         "landlord": self.land_lord.id,
    #         "property": self.property.id,
    #         "status": APPLICATION_STATUS.PENDING,
    #         "description": "Some Description"    
    #     }

    #     self.token_general_manager = Token.objects.create(
    #         user=self.general_manager)
    #     self.token_landlord = Token.objects.create(user=self.land_lord)
    #     self.token_tenant = Token.objects.create(user=self.tenant)
    #     self.token_listing_manager = Token.objects.create(
    #         user=self.listing_manager)

    # def test_create_application_by_general_manager_should_fail(self):
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
    #     response = self.client.post(
    #         self.applications_endpoint, self.test_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_create_application_by_land_lord_should_pass(self):
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
    #     response = self.client.post(self.applications_endpoint, self.test_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_create_application_by_tenant_should_pass(self):
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_tenant.key)
    #     response = self.client.post(self.applications_endpoint, self.test_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_get_application_details_by_id_by_landlord_should_pass(self):
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
    #     response = self.client.get(f"{self.applications_endpoint}{self.application.id}/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_all_applications_by_listing_manager_should_pass(self):
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_listing_manager.key)
    #     response = self.client.get(self.applications_endpoint)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_should_applications_update_property_detail(self):
    #     id = self.application.id
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
    #     response = self.client.patch(
    #         f"{self.applications_endpoint}{id}/", {"description": "updated description"}, format="json")
    #     data = response.data
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_should_update_application_detail(self):
    #     _id = self.application.id
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_listing_manager.key)
    #     self.test_data["description"] = "this is an updated description"
    #     response = self.client.put(f"{self.applications_endpoint}{_id}/", self.test_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["description"], self.test_data["description"])

    # def test_should_delete_application_by_manager(self):
    #     _id = self.application.id
    #     self.client.credentials(
    #         HTTP_AUTHORIZATION='Token ' + self.token_listing_manager.key)
    #     response = self.client.delete(f"{self.applications_endpoint}{_id}/")
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
