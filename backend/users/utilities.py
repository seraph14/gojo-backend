import vonage
import os
from django.db import models

class UserTypes(models.IntegerChoices):
    TENANT = 1
    LANDLORD = 2
    FINANCIAL_MANAGER = 3
    LISTING_MANAGER = 4
    GENERAL_MANAGER = 5

# def send_otp_to_phone(phone):
#     client = vonage.Client(os.environ["VONAGE_API_KEY"], secret=os.environ["VONAGE_API_SECRETE"])
#     verify = vonage.Verify(client)
#     response = verify.start_verification(number="+251" + phone[1:], brand="GOJO")

#     if response["status"] == "0":
#         return response["request_id"]
#     else:
#         raise Exception(response["error_text"])

# def verify_otp(request_id, code):
#     client = vonage.Client(os.environ["VONAGE_API_KEY"], secret=os.environ["VONAGE_API_SECRETE"])
#     verify = vonage.Verify(client)
    
#     response = verify.check(request_id=request_id, code=code)
#     if response["status"] == "0":
#         return (response["event_id"])
#     elif response["status"] == "6":
#         raise Exception("Already Verified")
#     else:
#         raise Exception("Expired")




import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])

def send_otp_to_phone(phone):
    verify.verifications.create(to="+251" + phone[1:], channel='sms')

def verify_otp(phone, code):
    try:
        result = verify.verification_checks.create(to="+251" + phone[1:], code=code)
    except TwilioRestException as e:
        raise Exception("Something went wrong")
    return result.status == 'approved'


def send_sms_message(user, password):
    print("sending================")
    client.messages \
                .create(
                     body=f"Welcome to GOJO, {user.first_name}. \n This is your new temporary pin: {password} \n Please change your password right away.",
                     from_='+13158886153',
                     to=f'+251{user.phone[1:]}',
                 )