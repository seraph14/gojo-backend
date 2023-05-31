from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def notify_new_unseen_chat(my_registration_token, sender, message):
    pass

def payment_arrived(r_token, user=None):
    data = FCMDevice.objects.send_message(
        Message(notification=Notification(title="Payment Received", body=f"Payment arrived")), additional_registration_ids=[r_token]
    )
    return FCMDevice.objects.create(registration_id=r_token, type="android")

def due_date_arrived(r_token, user=None):
    data = FCMDevice.objects.send_message(
        Message(notification=Notification(title="Due date arrived", body=f"Pay your rent in time!")), additional_registration_ids=[r_token]
    )
    return FCMDevice.objects.create(registration_id=r_token, type="android")

# LANDLORD
def withdrawal_request_approved(r_token, user=None):
    data = FCMDevice.objects.send_message(
        Message(notification=Notification(title="Withdrawal request", body=f"Your payment request has been approved!")), additional_registration_ids=[r_token]
    )
    return FCMDevice.objects.create(registration_id=r_token, type="android")

def withdrawal_request_denied(r_token, user=None):
    data = FCMDevice.objects.send_message(
        Message(notification=Notification(title="Withdrawal request", body=f"Your payment request has been denied!")), additional_registration_ids=[r_token]
    )
    return FCMDevice.objects.create(registration_id=r_token, type="android")


def new_message_arrived(r_token, user=None):
    data = FCMDevice.objects.send_message(
        Message(notification=Notification(title="New Message", body=f"You have a new unread message")), additional_registration_ids=[r_token]
    )
    
    return FCMDevice.objects.create(registration_id=r_token, type="android")
