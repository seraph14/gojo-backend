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
        self.tenant = User.objects.create(
            email="test@tenant.com",
            password="123123",
            first_name="Tenant",
            last_name="Natnael",
            role=UserTypes.TENANT,
            is_active=True,
            phone="0955211643",
            # phone_verified=True,
        )
        self.landlord = User.objects.create(
            email="test@landlord.com",
            password="123123",
            first_name="LandLord",
            last_name="Kidus",
            role=UserTypes.LANDLORD,
            is_active=True,
            phone="0955211643",
            # phone_verified=True
        )

        self.general = User.objects.create(
            email="test@general.com",
            password="123123",
            first_name="GeneralManager",
            last_name="Surafel",
            role=UserTypes.GENERAL_MANAGER,
            is_active=True,
            phone="0955211643",
            # phone_verified=True,
        )

        self.finance = User.objects.create(
            email="test@finance.com",
            password="123123",
            first_name="Finance",
            last_name="Nabek",
            role=UserTypes.FINANCIAL_MANAGER,
            is_active=True,
            phone="0955211643",
            # phone_verified=True,
        )

        self.listing = User.objects.create(
            email="test@listing.com",
            password="123123",
            first_name="Listing",
            last_name="Lingerew",
            role=UserTypes.LISTING_MANAGER,
            is_active=True,
            phone="0955211643",
            # phone_verified=True,
        )
        # self.user_attach_images()
        self.seed_properties()

    def user_attach_images(self):
        url = 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80'

        response = requests.get(url)

        if response.status_code == 200:
            image_file = self.generate_fake_image()

            self.landlord.avatar = image_file
            self.tenant.avatar = image_file
            self.listing.avatar = image_file
            self.finance.avatar = image_file
            self.general.avatar = image_file

            self.landlord.avatar.save()
            self.tenant.avatar.save()
            self.listing.avatar.save()
            self.finance.avatar.save()
            self.general.avatar.save()

            print("Avatar created successfully.")
        else:
            print("Failed to download avatar image.")

    def generate_fake_image(self):
        response = requests.get(
            f"https://picsum.photos/{random.choice(range(500, 4000))}/{random.choice(range(500, 4000))}",
            stream=True
        )
        if response.status_code == 200:
            temp_image = BytesIO(response.content)
            return File(temp_image)

        return None

    def seed_properties(self):
        property_obj = Property.objects.create(
            owner=self.tenant,
            availability=[datetime.now(), datetime.now()],
            category=[1, 2, 3],
            latitude=123.456789,
            longitude=987.654321,
            facilities={
                'rooms': 2,
                'size': {
                    "area": 23,
                    "scale": "ft"
                }}
        )

        data = self.generate_fake_image()
        property_image_obj = PropertyImage.objects.create(
            property=property_obj,
            image=data
        )

        print("PropertyImage created successfully.")
