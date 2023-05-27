import vonage
import os
from django.db import models

class UserTypes(models.IntegerChoices):
    TENANT = 1
    LANDLORD = 2
    FINANCIAL_MANAGER = 3
    LISTING_MANAGER = 4
    GENERAL_MANAGER = 5

# TODO: Resend needs to be tested
def send_otp_to_phone(phone):
    client = vonage.Client(os.environ["VONAGE_API_KEY"], secret=os.environ["VONAGE_API_SECRETE"])
    verify = vonage.Verify(client)
    response = verify.start_verification(number="+251" + phone[1:], brand="GOJO")

    if response["status"] == "0":
        return response["request_id"]
    else:
        raise Exception(response["error_text"])

# TODO: Resend needs to be tested
def verify_otp(request_id, code):
    client = vonage.Client(os.environ["VONAGE_API_KEY"], secret=os.environ["VONAGE_API_SECRETE"])
    verify = vonage.Verify(client)
    
    response = verify.check(request_id=request_id, code=code)
    if response["status"] == "0":
        return (response["event_id"])
    elif response["status"] == "6":
        raise Exception("Already Verified")
    else:
        raise Exception("Expired")

