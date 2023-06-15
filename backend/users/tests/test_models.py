from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from users.models import User
from users.utilities import UserTypes


class UserModelTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(
            phone="0955211651",
            email="test@tenant.com",
            password="123123",
            first_name="Tenant",
            last_name="Natnael",
            role=UserTypes.TENANT
        )

        User.objects.create_user(
            email="test@landlord.com",
            password="123123",
            phone="0955211655",
            first_name="LandLord",
            last_name="Kidus",
            role=UserTypes.LANDLORD
        )

    def test_user_creation(self):
        user = User.objects.create_user(
            email="test@lmanager.com",
            phone="0955211618",
            password="123123",
            first_name="Listing",
            last_name="Ling",
            role=UserTypes.LISTING_MANAGER
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, "test@lmanager.com")

    def test_should_query_all_users(self):
        users = User.objects.all().count()
        self.assertEqual(users, 2)

    def test_should_query_user_by_email(self):
        user = User.objects.get(email="test@tenant.com")
        self.assertEqual(user.email, "test@tenant.com")

    def test_should_change_user_status(self):
        user = User.objects.get(email="test@tenant.com")
        user.role = UserTypes.GENERAL_MANAGER
        user.save()
        self.assertEqual(user.role, UserTypes.GENERAL_MANAGER)
