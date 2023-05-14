from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from users.models import User
from users.utilities import UserTypes
from django.contrib.auth.hashers import make_password


class UserViewsTest(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.user_1 = User.objects.create_user(
            email="test@gmanager.com",
            password="123123",
            first_name="GManager",
            last_name="Natnael",
            role=UserTypes.GENERAL_MANAGER
        )
        self.user_2 = User.objects.create_user(
            email="test@landlord.com",
            password="123123",
            first_name="LandLord",
            last_name="Kidus",
            role=UserTypes.LANDLORD
        )
        self.token_general_manager = Token.objects.create(user=self.user_1)
        self.token_landlord = Token.objects.create(user=self.user_2)

    def test_create_manager_by_general_manager_should_pass(self):
        data = {
            "first_name": "Natnael",
            "last_name": "Abay",
            "email": "se.natnael.abay@gmail.com",
            "password": "123123",
            "role": UserTypes.FINANCIAL_MANAGER
        }
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
        response = self.client.post("/api/v1/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_manager_without_general_manager_fails(self):
        data = {
            "first_name": "Natnael",
            "last_name": "Abay",
            "email": "se.natnael.abay@gmail.com",
            "password": "123123",
            "role": UserTypes.FINANCIAL_MANAGER
        }
        response = self.client.post("/api/v1/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_normal_user(self):
        # Normal user being tenant or landlord
        data = {
            "first_name": "Natnael",
            "last_name": "Abay",
            "email": "se.natnael.abay@gmail.com",
            "password": "123123",
            "role": UserTypes.TENANT
        }
        response = self.client.post("/api/v1/users/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_current_user_details(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
        response = self.client.get("/api/v1/users/me/")
        self.assertContains(response, "user")

    def test_user_login(self):
        data = {
            'username': "test@landlord.com",
            'password': "123123"
        }
        response = self.client.post(
            '/api/v1/users/login/', data, format='json')
        self.assertContains(response, "token")

    def test_user_logout(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
        response = self.client.post("/api/v1/users/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(len(response.data.get("results")), 2)

    def test_get_one_user(self):
        id = self.user_1.id
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
        response = self.client.get(f"/api/v1/users/{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_should_pass_for_none_g_managers(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_user_should_for_none_g_managers(self):
        id = self.user_1.id
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
        response = self.client.get(f"/api/v1/users/{id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_partial_update_user_detail(self):
        id = self.user_2.id
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)
        response = self.client.patch(
            f"/api/v1/users/{id}/", {"first_name": "Changed_Name"}, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("first_name"), "Changed_Name")

    def test_should_partial_update_user_detail_by_general_manager(self):
        id = self.user_2.id
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_general_manager.key)
        response = self.client.patch(
            f"/api/v1/users/{id}/", {"first_name": "Changed_Name"}, format="json")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("first_name"), "Changed_Name")

    def test_should_update_user_detail(self):
        id = self.user_2.id
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_landlord.key)

        response = self.client.put(f"/api/v1/users/{id}/", {
            "first_name": "Changed_Name",
            "last_name": "ababe", 
            "email": "t@G.com", 
            "password": make_password("password"),
            "role": UserTypes.LANDLORD }, format="json")

        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("first_name"), "Changed_Name")
