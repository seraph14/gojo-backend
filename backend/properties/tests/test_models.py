from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from users.models import User
from users.permissions import UserTypes
from properties.models import Property

class UserModelTestCase(TestCase):

    def setUp(self):
        self.land_lord = User.objects.create(
            email="test@llord.com",
            password="123123",
            first_name="LandLord",
            last_name="Natnael",
            role=UserTypes.LANDLORD
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
            availability=[datetime().utcnow()],
            category=[1, 2, 3],
            latitude=38.8941,
            longitude=-77.0364,
            facilities=["Kitchen"]
        )

    def test_property_creation(self):
        property = Property.objects.create(
            owner=self.land_lord,
            availability=[datetime().utcnow()],
            category=[1, 2, 3],
            latitude=38.8951,
            longitude=-77.0364,
            facilities=["Bathroom"]
        )
        self.assertIsInstance(property, Property())
        self.assertEqual(property.owner.id, self.land_lord.id)

    def test_should_query_all_properties(self):
        properties = Property.objects.all().count()
        self.assertEqual(properties, 1)

    def test_should_query_user_by_owner(self):
        property = Property.objects.get(owner=self.land_lord)
        self.assertEqual(property.owner, self.land_lord)