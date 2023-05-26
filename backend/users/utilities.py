import vonage
from django.db import models

class UserTypes(models.IntegerChoices):
    TENANT = 1
    LANDLORD = 2
    FINANCIAL_MANAGER = 3
    LISTING_MANAGER = 4
    GENERAL_MANAGER = 5

def send_otp_to_phone(phone):
    client = vonage.Client(key="544c8839", secret="CEqbQW23LZ95onBL")
    verify = vonage.Verify(client)
    response = verify.start_verification(number=phone, brand="GOJO Rental Services")

    if response["status"] == "0":
        return response["request_id"]
    else:
        raise Exception(response["error_text"])

def verify_otp(request_id, code):
    client = vonage.Client(key="544c8839", secret="CEqbQW23LZ95onBL")
    verify = vonage.Verify(client)
    response = verify.start_verification(number=phone, brand="GOJO Rental Services")

    response = verify.check(REQUEST_ID, code=CODE)
    if response["status"] == "0":
        return (response["event_id"])
    else:
        raise Exception(response["error_text"])
