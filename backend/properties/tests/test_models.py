from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from users.models import User
from users.permissions import UserTypes
from properties.models import Property

class UserModelTestCase(TestCase):

    def setUp(self):
        from properties.models import Category
        self.apartment = Category.objects.create(name="Apartment")
        self.studio = Category.objects.create(name="Studio")
        self.vila = Category.objects.create(name="Vila")
        self.condo = Category.objects.create(name="Condo")
        self.office = Category.objects.create(name="Office")
        self.warehouse = Category.objects.create(name="Warehouse")

        self.land_lord = User.objects.create(
            email="test@llord.com",
            password="123123",
            first_name="LandLord",
            phone="0955211615",
            last_name="Natnael",
            role=UserTypes.LANDLORD
        )

        self.general_manager = User.objects.create(
            email="test@general.com",
            password="123123",
            first_name="general",
            last_name="Kidus",
            phone="0955224652",
            role=UserTypes.GENERAL_MANAGER
        )

        self.property = Property.objects.create(
            owner=self.land_lord,
            visiting_hours=[
                {
                    "day": "Monday",
                    "from": "9:00 AM",
                    "to": "11:00 AM"
                },
                {
                    "day": "Tuesday",
                    "from": "11:00 AM",
                    "to": "1:00 PM"
                }
            ],
            title="Test Title",
            amount=4000,
            category=self.condo,
            is_approved=True,
            description="Lorem ipsum lorem ipsum"
        )

    def test_property_creation(self):
        property = Property.objects.create(
            owner=self.land_lord,
            visiting_hours=[
                {
                    "day": "Monday",
                    "from": "9:00 AM",
                    "to": "11:00 AM"
                },
                {
                    "day": "Tuesday",
                    "from": "11:00 AM",
                    "to": "1:00 PM"
                }
            ],
            title="Test Title",
            amount=4000,
            category=self.condo,
            is_approved=True,
            description="Lorem ipsum lorem ipsum"
        )
        self.assertIsInstance(property, Property)
        self.assertEqual(property.owner.id, self.land_lord.id)

    def test_should_query_all_properties(self):
        properties = Property.objects.all().count()
        self.assertEqual(properties, 1)

    def test_should_query_user_by_owner(self):
        property = Property.objects.get(owner=self.land_lord)
        self.assertEqual(property.owner, self.land_lord)