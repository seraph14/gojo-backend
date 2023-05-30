import requests
import tempfile
import random
from io import BytesIO
from datetime import datetime
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand, CommandError
from django.core import files
from users.models import User
from users.utilities import UserTypes
from properties.models import Property, PropertyImage


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.tenant = User.objects.create_user(
            email="test@tenant.com",
            password="123123",
            first_name="Surafel",
            last_name="Kassahun",
            role=UserTypes.TENANT,
            is_active=True,
            phone="0949024607",
            is_verified=True
            # phone_verified=True,
        )
        # self.tenant = User.objects.get(phone="0949024607")
        self.landlord = User.objects.create_user(
            email="test@landlord.com",
            password="123",
            first_name="Natnael",
            last_name="Abay",
            role=UserTypes.LANDLORD,
            is_active=True,
            phone="0918012730",
            is_verified=True
        )

        self.landlord = User.objects.create_user(
            email="test@landlord.com",
            password="123",
            first_name="Kidus",
            last_name="Yoseph",
            role=UserTypes.LANDLORD,
            is_active=True,
            phone="0972476097",
            is_verified=True
        )

        # self.landlord = User.objects.get(phone='0918012730')

        from chat.models import Message, Thread

        thread = Thread.objects.create(
            user_1=self.tenant,
            user_2=self.landlord
        )

        chat = Message.objects.create(
            thread=thread,
            content="This is a fake message! and the landlords side!",
            sender=self.landlord,
            seen=True,
        )

        # self.seed_property_v2()
        # self.seed_pending_transactions()

        self.seed_facilities()
        self.seed_category()
        self.seed_properties_full()
        self.seed_applications()
        self.seed_appointments()
        self.seed_virtual_tour()

        # self.general = User.objects.create_user(
        #     email="test@general.com",
        #     password="123123",
        #     first_name="GeneralManager",
        #     last_name="Lingerew",
        #     role=UserTypes.GENERAL_MANAGER,
        #     is_active=True,
        #     phone="0943447499",
        #     # phone_verified=True,
        # )

        # self.finance = User.objects.create_user(
        #     email="test@finance.com",
        #     password="123123",
        #     first_name="Finance",
        #     last_name="Nabek",
        #     role=UserTypes.FINANCIAL_MANAGER,
        #     is_active=True,
        #     phone="0915207146",
        #     # phone_verified=True,
        # )

        # self.listing = User.objects.create_user(
        #     email="test@listing.com",
        #     password="123123",
        #     first_name="Listing",
        #     last_name="Lingerew",
        #     role=UserTypes.LISTING_MANAGER,
        #     is_active=True,
        #     phone="0918704962",
        #     # phone_verified=True,
        # )
        # # self.user_attach_images()
        # self.seed_properties()

    def seed_property_v2(self):
        from properties.models import Property
        from transactions.models import UserRentedProperties, PROPERTY_RENT_STATUS
        from faker import Faker
        fake = Faker()

        self.property = Property.objects.create(
            owner=self.landlord,
            visiting_hours=[
                {
                    "day": "Monday",
                    "from": 9,
                    "to": 11
                },
                {
                    "day": "Tuesday",
                    "from": 11,
                    "to": 13
                }
            ],
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            amount=8000
        )

        self.userRentedProperties = UserRentedProperties.objects.create(
            property=self.property,
            start_date="2020-10-10",
            user=self.tenant,
            status=PROPERTY_RENT_STATUS.ONGOING
        )

    def seed_pending_transactions(self):
        from transactions.models import Transaction
        from transactions.utils import TRANSACTION_STATUS, TRANSACTION_TYPE

        # transaction for pending payment [rent]
        transaction = Transaction.objects.create(
            sender=self.tenant,
            status=TRANSACTION_STATUS.PENDING,
            type=TRANSACTION_TYPE.RENT_PAYMENT,
            rent_detail=self.userRentedProperties,
            amount=self.userRentedProperties.property.amount,
            payment_date=self.userRentedProperties.start_date
        )

    def seed_facilities(self):
        from properties.models import Facility
        self.facility_1 = Facility.objects.create(name="Bed rooms")
        self.facility_2 = Facility.objects.create(name="Square Area")

    def seed_category(self):
        from properties.models import Category
        self.apartment = Category.objects.create(name="Apartment")
        self.studio = Category.objects.create(name="Studio")
        self.vila = Category.objects.create(name="Vila")
        self.condo = Category.objects.create(name="Condo")
        self.office = Category.objects.create(name="Office")
        self.warehouse = Category.objects.create(name="Warehouse")

    def seed_properties_full(self):
        from properties.models import Property, Category, Facility, PropertyFacility, PropertyLocation
        from transactions.models import UserRentedProperties, PROPERTY_RENT_STATUS
        from faker import Faker
        fake = Faker()

        # property 1

        self.property_1 = Property.objects.create(
            owner=self.landlord,
            visiting_hours=[
                {
                    "day": "Monday",
                    "from": 9,
                    "to": 11
                },
                {
                    "day": "Tuesday",
                    "from": 11,
                    "to": 13
                }
            ],
            title="Test Title",
            amount=8000,
            category=self.condo,
            is_approved=True
        )

        self.location_1 = PropertyLocation.objects.create(
            name="Fake Address",
            latitude=(fake.latitude()),
            longitude=(fake.longitude()),
            property=self.property_1
        )

        self.property_1_facility = PropertyFacility.objects.create(
            property=self.property_1,
            facility=self.facility_1,
            count=20
        )

        self.property_1_facility_2 = PropertyFacility.objects.create(
            property=self.property_1,
            facility=self.facility_2,
            count=25
        )

        self.property_1.facilities.add(
            self.property_1_facility, self.property_1_facility_2)

        # property 2

        self.property_2 = Property.objects.create(
            owner=self.landlord,
            visiting_hours=[
                {
                    "day": "Monday",
                    "from": 9,
                    "to": 11
                },
                {
                    "day": "Tuesday",
                    "from": 11,
                    "to": 13
                }
            ],
            title="Test Title 2",
            amount=8000,
            category=self.studio,
            is_approved=True
        )

        self.location_2 = PropertyLocation.objects.create(
            name="Fake Address 2",
            latitude=(fake.latitude()),
            longitude=(fake.longitude()),
            property=self.property_2
        )

        self.property_2_facility = PropertyFacility.objects.create(
            property=self.property_2,
            facility=self.facility_1,
            count=20
        )

        self.property_2_facility_2 = PropertyFacility.objects.create(
            property=self.property_2,
            facility=self.facility_2,
            count=25
        )

        self.property_2.facilities.add(
            self.property_1_facility, self.property_2_facility_2)

        # property 3

        self.property_3 = Property.objects.create(
            owner=self.landlord,
            visiting_hours=[
                {
                    "day": "Monday",
                    "from": 9,
                    "to": 11
                },
                {
                    "day": "Tuesday",
                    "from": 11,
                    "to": 13
                }
            ],
            title="Test Title 3",
            amount=8000,
            category=self.studio,
            is_approved=True
        )

        self.location_3 = PropertyLocation.objects.create(
            name="Fake Address 3",
            latitude=(fake.latitude()),
            longitude=(fake.longitude()),
            property=self.property_3
        )

        self.property_3_facility = PropertyFacility.objects.create(
            property=self.property_3,
            facility=self.facility_1,
            count=20
        )

        self.property_3_facility_2 = PropertyFacility.objects.create(
            property=self.property_3,
            facility=self.facility_2,
            count=25
        )

        self.property_3.facilities.add(
            self.property_3_facility, self.property_3_facility_2)

        # property 4

        self.property_4 = Property.objects.create(
            owner=self.landlord,
            visiting_hours=[
                {
                    "day": "Monday",
                    "from": 9,
                    "to": 11
                },
                {
                    "day": "Tuesday",
                    "from": 11,
                    "to": 13
                }
            ],
            title="Test Title 4",
            amount=8000,
            category=self.studio,
            is_approved=True
        )

        self.location_4 = PropertyLocation.objects.create(
            name="Fake Address 4",
            latitude=(fake.latitude()),
            longitude=(fake.longitude()),
            property=self.property_4
        )

        self.property_4_facility = PropertyFacility.objects.create(
            property=self.property_4,
            facility=self.facility_1,
            count=20
        )

        self.property_4_facility_2 = PropertyFacility.objects.create(
            property=self.property_4,
            facility=self.facility_2,
            count=25
        )

        self.property_4.facilities.add(
            self.property_4_facility, self.property_4_facility_2)

    def seed_applications(self):
        from applications.models import Application
        from applications.utilities import APPLICATION_STATUS

        self.application_pending = Application.objects.create(
            tenant=self.tenant,
            status=APPLICATION_STATUS.PENDING,
            property=self.property_1,
            possible_start_date="2023-07-25",
            how_long=5,
            description="[approved] Some description why you want to get this house."
        )

        self.application_approved = Application.objects.create(
            tenant=self.tenant,
            status=APPLICATION_STATUS.APPROVED,
            property=self.property_2,
            possible_start_date="2023-07-25",
            how_long=5,
            description="[approved] Some description why you want to get this house."
        )

        self.application_withdrawn = Application.objects.create(
            tenant=self.tenant,
            status=APPLICATION_STATUS.WITHDRAWN,
            property=self.property_3,
            possible_start_date="2023-07-25",
            how_long=5,
            description="[withdrawn] Some description why you want to get this house."
        )

        self.application_rejected = Application.objects.create(
            tenant=self.tenant,
            status=APPLICATION_STATUS.REJECTED,
            property=self.property_4,
            possible_start_date="2023-07-25",
            how_long=5,
            description="[rejected] Some description why you want to get this house."

        )

    def seed_appointments(self):
        from appointments.models import Appointment
        from appointments.utils import APPOINTMENT_STATUS

        self.appointment_1 = Appointment.objects.create(
            status=APPOINTMENT_STATUS.PENDING,
            property=self.property_1,
            tenant=self.tenant,
            appointment_date="2023-06-10T12:00",
        )

        self.appointment_2 = Appointment.objects.create(
            status=APPOINTMENT_STATUS.APPROVED,
            property=self.property_2,
            tenant=self.tenant,
            appointment_date="2023-06-10T12:00",
        )

        self.appointment_3 = Appointment.objects.create(
            status=APPOINTMENT_STATUS.APPROVED,
            property=self.property_3,
            tenant=self.tenant,
            appointment_date="2023-06-10T12:00",
        )

        self.appointment_4 = Appointment.objects.create(
            status=APPOINTMENT_STATUS.CANCELED,
            property=self.property_4,
            tenant=self.tenant,
            appointment_date="2023-06-10T12:00",
        )

    def seed_virtual_tour(self):
        import uuid
        from decimal import Decimal
        from properties.models import Link, Marker, HotspotNode, VirtualTour
        from faker import Faker

        faker = Faker()
        uuid_4 = uuid.uuid4()
        uuid_4_2 = uuid.uuid4()

        print("====================== ", uuid_4)
        print("====================== ", uuid_4_2)

        self.virtual_tour = VirtualTour.objects.create(
            property=self.property_1,
            defaultViewPosition_latitude=faker.latitude(),
            defaultViewPosition_longitude=faker.longitude(),
            initialView=uuid_4
        )

        self.hotspot_node = HotspotNode.objects.create(
            id=uuid_4,
            panorama="/home/nati/Desktop/1674411002858.jpeg",
            virtual_tour=self.virtual_tour
        )

        self.hotspot_node_2 = HotspotNode.objects.create(
            id=uuid_4_2,
            panorama="/home/nati/Desktop/1674411002858.jpeg",
            virtual_tour=self.virtual_tour
        )

        self.virtual_tour.hotspotNodes.set(
            [self.hotspot_node, self.hotspot_node_2])

        self.link = Link.objects.create(
            nodeId=uuid_4_2,
            latitude=faker.latitude(),
            longitude=faker.longitude(),
            node=self.hotspot_node
        )

        self.link_2 = Link.objects.create(
            nodeId=uuid_4,
            latitude=faker.latitude(),
            longitude=faker.longitude(),
            node=self.hotspot_node_2
        )

        self.hotspot_node.links.set([self.link])
        self.hotspot_node_2.links.set([self.link_2])

        self.marker = Marker.objects.create(
            id=uuid.uuid4(),
            linksTo=uuid_4_2,
            tooltip="Move to the next scene",
            width=48,
            height=48,
            longitude=faker.latitude(),
            latitude=faker.longitude(),
            anchor="center",
            node=self.hotspot_node
        )

        self.marker_2 = Marker.objects.create(
            id=uuid.uuid4(),
            linksTo=uuid_4,
            tooltip="Move to the next scene",
            width=48,
            height=48,
            longitude=faker.latitude(),
            latitude=faker.longitude(),
            anchor="center",
            node=self.hotspot_node_2
        )

        self.hotspot_node.markers.set([self.marker])
        self.hotspot_node_2.markers.set([self.marker_2])
