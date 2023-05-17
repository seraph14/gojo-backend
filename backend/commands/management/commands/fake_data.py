from django.core.management.base import BaseCommand, CommandError
from users.models import User
from users.utilities import UserTypes


class Command(BaseCommand):
        
    def handle(self, *args, **options):
        User.objects.update_or_create(
            email="test@tenant.com",
            password="123123",
            first_name="Tenant",
            last_name="Natnael",
            role=UserTypes.TENANT
        )
        User.objects.update_or_create(
            email="test@landlord.com",
            password="123123",
            first_name="LandLord",
            last_name="Kidus",
            role=UserTypes.LANDLORD
        )

        User.objects.update_or_create(
            email="test@general.com",
            password="123123",
            first_name="GeneralManager",
            last_name="Surafel",
            role=UserTypes.GENERAL_MANAGER
        )

        User.objects.update_or_create(
            email="test@finance.com",
            password="123123",
            first_name="Finance",
            last_name="Nabek",
            role=UserTypes.FINANCIAL_MANAGER
        )

        User.objects.update_or_create(
            email="test@listing.com",
            password="123123",
            first_name="Listing",
            last_name="Lingerew",
            role=UserTypes.LISTING_MANAGER
        )


