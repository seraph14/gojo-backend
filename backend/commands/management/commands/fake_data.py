import requests
from datetime import datetime
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from users.models import User
from users.utilities import UserTypes
from properties.models import Property, PropertyImage



class Command(BaseCommand):

    def handle(self, *args, **options):
        self.tenant = User.objects.update_or_create(
            email="test@tenant.com",
            password="123123",
            first_name="Tenant",
            last_name="Natnael",
            role=UserTypes.TENANT
        )
        self.landlord = User.objects.update_or_create(
            email="test@landlord.com",
            password="123123",
            first_name="LandLord",
            last_name="Kidus",
            role=UserTypes.LANDLORD
        )

        self.general = User.objects.update_or_create(
            email="test@general.com",
            password="123123",
            first_name="GeneralManager",
            last_name="Surafel",
            role=UserTypes.GENERAL_MANAGER
        )

        self.finance = User.objects.update_or_create(
            email="test@finance.com",
            password="123123",
            first_name="Finance",
            last_name="Nabek",
            role=UserTypes.FINANCIAL_MANAGER
        )

        self.listing = User.objects.update_or_create(
            email="test@listing.com",
            password="123123",
            first_name="Listing",
            last_name="Lingerew",
            role=UserTypes.LISTING_MANAGER
        )
        self.seed_properties()

    def seed_properties(self):
        property_obj = Property(
            owner=self.tenant,
            availability=[datetime.utcnow(), datetime.utcnow()],
            category=[1, 2, 3],  
            latitude=123.456789,
            longitude=987.654321,
            facilities={'rooms': 2, 'size': {
                "area": 23,
                "scale" : "ft"
            } }
        )

        img_url = [
            'https://images.unsplash.com/photo-1566601146613-82f9dbd68995?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80'
            'https://images.unsplash.com/photo-1571781418606-70265b9cce90?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
            'https://images.unsplash.com/photo-1616047006789-b7af5afb8c20?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80'
        ]
        
        for url in img_url:
            response = requests.get(url)

            if response.status_code == 200:
                property_image_obj = PropertyImage(property=property_obj)

                image_file = File(response.content)

                property_image_obj.image.save(f"{property_image_obj.id}.jpg", image_file)

                property_image_obj.save()

                print("PropertyImage created successfully.")
            else:
                print("Failed to download the image.")


