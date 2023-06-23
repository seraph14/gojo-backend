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
        # self.tenant = User.objects.create_user(
        #     email="test@tenant.com",
        #     password="123123",
        #     first_name="Surafel",
        #     last_name="Kassahun",
        #     role=UserTypes.TENANT,
        #     is_active=True,
        #     phone="0949024607",
        #     is_verified=True
        # )
        
        # self.landlord = User.objects.create_user(
        #     email="test@landlord.com",
        #     password="123",
        #     first_name="LandlordTesting",
        #     last_name="Yes",
        #     role=UserTypes.LANDLORD,
        #     is_active=True,
        #     phone="0918012730",
        #     is_verified=True
        # )

        # from users.models import AccountBalance

        # AccountBalance.objects.create(user=self.landlord)

        # self.landlord_test_kidus = User.objects.create_user(
        #     email="test@landlord.com",
        #     password="123",
        #     first_name="Kidus",
        #     last_name="Yoseph",
        #     role=UserTypes.LANDLORD,
        #     is_active=True,
        #     phone="0972476097",
        #     is_verified=True
        # )

        # AccountBalance.objects.create(user=self.landlord_test_kidus)
        self.landlord_linge = User.objects.create_user(
            email="test@listing.com",
            password="123123",
            first_name="Abebe",
            last_name="Alemu",
            role=UserTypes.LISTING_MANAGER,
            is_active=True,
            phone="0943447400",
            is_verified=True
        )

        self.landlord_linge = User.objects.create_user(
            email="test@financial.com",
            password="123123",
            first_name="Abdi",
            last_name="Natneam",
            role=UserTypes.FINANCIAL_MANAGER,
            is_active=True,
            phone="0943447401",
            is_verified=True
        )

        self.landlord_linge = User.objects.create_user(
            email="test@general.com",
            password="123123",
            first_name="Lingerew",
            last_name="Getie",
            role=UserTypes.GENERAL_MANAGER,
            is_active=True,
            phone="0943447402",
            is_verified=True
        )

        # # self.landlord = User.objects.get(phone='0918012730')

        # from chat.models import Message, Thread

        # thread = Thread.objects.create(
        #     tenant=self.tenant,
        #     landlord=self.landlord
        # )

        # chat = Message.objects.create(
        #     thread=thread,
        #     content="This ia ma message from the landlord!",
        #     sender=self.landlord,
        #     seen=True,
        # )

        # chat = Message.objects.create(
        #     thread=thread,
        #     content="This ia a message from the tenant!",
        #     sender=self.tenant,
        #     seen=True,
        # )

        self.seed_facilities()
        self.seed_category()
        # self.seed_properties_full()
        # self.seed_applications()
        # self.seed_appointments()
        # self.seed_virtual_tour()
        # self.seed_review()
        # self.seed_landlord_transactions()

     

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
                    "from": "9:00 PM",
                    "to": "12:00 AM"
                },
                {
                    "day": "Tuesday",
                    "from": "11:00 AM",
                    "to": "12:00 AM"
                }
            ],
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            amount=8000,
            description="Lorem ipsum lorem ipsum"
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
        self.facility_1 = Facility.objects.create(name="Bedroom")
        self.facility_2 = Facility.objects.create(name="Bathroom")
        self.facility_3 = Facility.objects.create(name="Square area")

    def seed_category(self):
        from properties.models import Category
        self.apartment = Category.objects.create(name="Apartment")
        self.studio = Category.objects.create(name="Studio")
        self.vila = Category.objects.create(name="Vila")
        self.condo = Category.objects.create(name="Condo")
        self.office = Category.objects.create(name="Office")
        self.warehouse = Category.objects.create(name="Warehouse")

    def seed_properties_full(self):
        from properties.models import Property, Category, Facility, PropertyFacility, PropertyLocation, Favorites
        from transactions.models import UserRentedProperties, PROPERTY_RENT_STATUS
        from faker import Faker
        fake = Faker()

        # property 1

        self.property_1 = Property.objects.create(
            owner=self.landlord,
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

        (Favorites.objects.create(
            property=self.property_1,
            user=self.tenant
        ))
        self.location_1 = PropertyLocation.objects.create(
            street="Fake Address",
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

        self.property_1_facility_3 = PropertyFacility.objects.create(
            property=self.property_1,
            facility=self.facility_3,
            count=859
        )
        self.userRentedProperties_1 = UserRentedProperties.objects.create(
            property=self.property_1,
            start_date="2020-10-10",
            user=self.tenant,
            status=PROPERTY_RENT_STATUS.ONGOING
        )
        self.property_1.facilities.add(
            self.property_1_facility, self.property_1_facility_2)

        # property 2

        self.property_2 = Property.objects.create(
            owner=self.landlord,
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
            title="Test Title 2",
            amount=1000,
            category=self.studio,
            is_approved=True,
            description="Lorem ipsum lorem ipsum"
        )

        self.location_2 = PropertyLocation.objects.create(
            street="Fake Address 2",
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

        self.property_2_facility_3 = PropertyFacility.objects.create(
            property=self.property_2,
            facility=self.facility_3,
            count=2785
        )

        self.property_2.facilities.add(
            self.property_1_facility, self.property_2_facility_2, self.property_2_facility_3)

        # self.userRentedProperties_3 = UserRentedProperties.objects.create(
        #     property=self.property_2,
        #     start_date="2020-10-10",
        #     user=self.tenant,
        #     status=PROPERTY_RENT_STATUS.ONGOING
        # )
        # property 3

        self.property_3 = Property.objects.create(
            owner=self.landlord,
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
            title="Test Title 3",
            amount=800,
            category=self.studio,
            is_approved=True,
            description="Lorem ipsum lorem ipsum"
        )

        self.location_3 = PropertyLocation.objects.create(
            street="Fake Address 3",
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
        
        self.property_3_facility_3 = PropertyFacility.objects.create(
            property=self.property_3,
            facility=self.facility_3,
            count=987
        )

        # self.userRentedProperties_3 = UserRentedProperties.objects.create(
        #     property=self.property_3,
        #     start_date="2020-10-10",
        #     user=self.tenant,
        #     status=PROPERTY_RENT_STATUS.ONGOING
        # )
        self.property_3.facilities.add(
            self.property_3_facility, self.property_3_facility_2, self.property_3_facility_3)

        # property 4

        self.property_4 = Property.objects.create(
            owner=self.landlord,
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
            title="Test Title 4",
            amount=9000,
            category=self.studio,
            is_approved=True,
            description="Lorem ipsum lorem ipsum"
        )

        self.location_4 = PropertyLocation.objects.create(
            street="Fake Address 4",
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

        self.property_4_facility_3 = PropertyFacility.objects.create(
            property=self.property_4,
            facility=self.facility_3,
            count=500
        )

        # self.userRentedProperties_4 = UserRentedProperties.objects.create(
        #     property=self.property_4,
        #     start_date="2020-10-10",
        #     user=self.tenant,
        #     status=PROPERTY_RENT_STATUS.ONGOING
        # )
        self.property_4.facilities.add(
            self.property_4_facility, self.property_4_facility_2, self.property_4_facility_3)
        
        print("================ image upload started ============")
        self.image_1 = PropertyImage.objects.create(
            image=self.download_image("https://images.pexels.com/photos/4067759/pexels-photo-4067759.jpeg"),
            property=self.property_1
        )

        self.image_1 = PropertyImage.objects.create(
            image=self.download_image("https://images.pexels.com/photos/4067759/pexels-photo-4067759.jpeg"),
            property=self.property_1
        )
        
        self.image_1 = PropertyImage.objects.create(
            image=self.download_image("https://images.pexels.com/photos/4067759/pexels-photo-4067759.jpeg"),
            property=self.property_1
        )
        
        self.image_1 = PropertyImage.objects.create(
            image=self.download_image("https://images.pexels.com/photos/4067759/pexels-photo-4067759.jpeg"),
            property=self.property_1
        )
        print("============ image upload 1 ==============")

        self.image_1 = PropertyImage.objects.create(
            image=self.download_image("https://images.pexels.com/photos/4067759/pexels-photo-4067759.jpeg"),
            property=self.property_2
        )
        print("============ image upload 2 ==============")

        self.image_1 = PropertyImage.objects.create(
            image=self.download_image("https://images.pexels.com/photos/4067759/pexels-photo-4067759.jpeg"),
            property=self.property_3
        )
        print("============ image upload 3 ==============")

        self.image_1 = PropertyImage.objects.create(
            image=self.download_image("https://images.pexels.com/photos/4067759/pexels-photo-4067759.jpeg"),
            property=self.property_4
        )
        print("============ image upload 4 ==============")


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
            status=APPLICATION_STATUS.PENDING,
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

        self.virtual_tour = VirtualTour.objects.create(
            property=self.property_1,
            defaultViewPosition_latitude=faker.latitude(),
            defaultViewPosition_longitude=faker.longitude(),
            initialView=uuid_4
        )

        self.hotspot_node = HotspotNode.objects.create(
            id=uuid_4,
            panorama="/panorama_images/1.jpg",
            virtual_tour=self.virtual_tour
        )

        self.hotspot_node_2 = HotspotNode.objects.create(
            id=uuid_4_2,
            panorama="/panorama_images/2.jpg",
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


    def download_image(self, url):
        import requests
        from django.core.files.base import ContentFile
        import uuid
        response = requests.get(url)
        content = response.content
        image_file = ContentFile(content, name=str(uuid.uuid4()))
        return image_file

    def seed_review(self):
        from reviews.models import Review
        self.review_1 = Review.objects.create(
            property=self.property_1,
            user=self.tenant,
            comment="Te rating data is being fetched",
            rating=5
        )

        self.review_2 = Review.objects.create(
            property=self.property_2,
            user=self.tenant,
            comment="Te rating data is being fetched",
            rating=3
        )

        self.review_3 = Review.objects.create(
            property=self.property_3,
            user=self.tenant,
            comment="Te rating data is being fetched",
            rating=4
        )

    def seed_landlord_transactions(self):
        from transactions.models import Transaction
        from transactions.utils import TRANSACTION_STATUS, TRANSACTION_TYPE

        transaction = Transaction.objects.create(
            sender=self.tenant,
            receiver=self.landlord_test_kidus,
            status=TRANSACTION_STATUS.PAID,
            type=TRANSACTION_TYPE.RENT_PAYMENT,
            rent_detail=self.userRentedProperties_1,
            amount=self.userRentedProperties_1.property.amount,
            payment_date=self.userRentedProperties_1.start_date
        )

        # transaction for pending payment [rent]
        transaction = Transaction.objects.create(
            sender=self.landlord_test_kidus,
            status=TRANSACTION_STATUS.PENDING,
            type=TRANSACTION_TYPE.WITHDRAWAL,
            rent_detail=self.userRentedProperties_1,
            amount=self.userRentedProperties_1.property.amount,
            payment_date=self.userRentedProperties_1.start_date
        )

        transaction = Transaction.objects.create(
            sender=self.landlord_test_kidus,
            status=TRANSACTION_STATUS.WITHDRAWAL_REQUEST_APPROVED,
            type=TRANSACTION_TYPE.WITHDRAWAL,
            rent_detail=self.userRentedProperties_1,
            amount=self.userRentedProperties_1.property.amount,
            payment_date=self.userRentedProperties_1.start_date
        )

        transaction = Transaction.objects.create(
            sender=self.landlord_test_kidus,
            status=TRANSACTION_STATUS.WITHDRAWAL_REQUEST_DENIED,
            type=TRANSACTION_TYPE.WITHDRAWAL,
            rent_detail=self.userRentedProperties_1,
            amount=self.userRentedProperties_1.property.amount,
            payment_date=self.userRentedProperties_1.start_date
        )

        transaction = Transaction.objects.create(
            sender=self.landlord_test_kidus,
            status=TRANSACTION_STATUS.WITHDRAWAL_REQUEST_DENIED,
            type=TRANSACTION_TYPE.WITHDRAWAL,
            rent_detail=self.userRentedProperties_1,
            amount=self.userRentedProperties_1.property.amount,
            payment_date=self.userRentedProperties_1.start_date
        )

