from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from users.utilities import UserTypes
class MyEndToEndTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tenant = User.objects.create_user(
            phone="0955211651",
            email="test@tenant.com",
            password="123123",
            first_name="Tenant",
            last_name="Natnael",
            role=UserTypes.TENANT
        )

        self.landlord = User.objects.create_user(
            email="test@landlord.com",
            password="123123",
            phone="0955211655",
            first_name="LandLord",
            last_name="Kidus",
            role=UserTypes.LANDLORD
        )


    # def test_end_to_end_flow(self):

    #     response = self.client.post("api/v1/users/tenant_login/", {'username': self.tenant.phone, 'password': "123123"}, format='json')
        
    #     print("response.data", response)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     token = response.data['user']["token"]
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    #     response = self.client.get("api/v1/users/me/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     response = self.client.post("api/v1/users/logout/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
