import os
import requests
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, permission_classes
from users.models import User
from properties.models import Property
from users.serializers import UserSerializer
from users.utilities import UserTypes
from users.permissions import *
from transactions.models import Transaction
from backend.utilities import payment_arrived, rent_paid

class ChapaUtils:
    CHAPA_PUBLIC = os.environ.get("CHAPA_TEST_PUBLIC_KEY", "chapa_public")
    CHAPA_SECRET = os.environ.get("CHAPA_TEST_SECRET_KEY", "chapa_private")
    CALLBACK_URL = os.environ.get("CHAPA_CALLBACK_URL", "http://google.com")
    CHAPA_TRANSACTIONS_URL = "https://api.chapa.co/v1/transaction/"
    
    headers = {
        "Authorization": f"Bearer {CHAPA_SECRET}",
        "Content-type": "application/json",
    }
    @classmethod
    def initialize(self, amount, email, first_name, last_name, ref, **kwargs):
        request = requests.post(
            self.CHAPA_TRANSACTIONS_URL + 'initialize', json={
                "amount": str(amount),
                "currency" : "ETB",
                "first_name" : first_name,
                "last_name": last_name,
                "tx_ref" : ref,
                "callback_url" : self.CALLBACK_URL,
                "customization[title]" : "GOJO Rental Services",
                "customization[description]" : "Pay UP!",
            },
            headers=self.headers
        )
        return request.json()

@api_view(["GET"])
@permission_classes([AllowAny])
def verify_payment_status(request):
    tx_ref = "Proper"
    request = requests.get(ChapaUtils.CHAPA_TRANSACTIONS_URL + f"verify/{tx_ref}", headers=ChapaUtils.headers)
    data = request.json()
    if data["status"] == "success":
        transaction = Transaction.objects.get(tx_ref=tx_ref)
        
        rent_paid(r_token)

        payment_arrived(r_token)
        return Response()