from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from users.models import User
from users.permissions import UserTypes
from applications.models import Application
from applications.utilities import APPLICATION_STATUS
from properties.models import Property

class ApplicationModelTestCase(TestCase):
    def setUp(self):
        self.tenant_email = "test@tenant.com"
        self.landlord_email = "test@landlord.com"
        self.manager_email = "test@lmanager.com"
        self.description = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."

        self.tenant = User.objects.create(
            email=self.tenant_email,
            password="123123",
            phone="0955211655",
            first_name="Tenant",
            last_name="Natnael",
            role=UserTypes.TENANT
        )

        self.landlord = User.objects.create(
            email=self.landlord_email,
            phone="0955211651",
            password="123123",
            first_name="LandLord",
            last_name="Kidus",
            role=UserTypes.LANDLORD
        )
        self.property = Property.objects.create(
            owner=self.landlord,
            availability=["2020-10-10T12:00:00Z"],
            category=[1, 2, 3],
            latitude=38.8941,
            longitude=-77.0364,
            facilities=["Kitchen"]
        )

    def test_application_creation(self):
        _application = Application.objects.create(
            description=self.description,
            tenant=self.tenant,
            landlord=self.landlord,
            status=APPLICATION_STATUS.SIGNED,
            property=self.property
        )
        self.assertIsInstance(_application, Application)

    def test_should_query_all_applications(self):
        _applications = Application.objects.all().count()
        self.assertEqual(_applications, 0)

    def test_should_change_application_status(self):
        _application = Application.objects.create(
            description=self.description,
            tenant=self.tenant,
            landlord=self.landlord,
            status=APPLICATION_STATUS.SIGNED,
            property=self.property
        )
        _application.status = APPLICATION_STATUS.REVOKED
        _application.save()
        self.assertEqual(_application.status, APPLICATION_STATUS.REVOKED)
