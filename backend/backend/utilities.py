from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def notify_new_unseen_chat(my_registration_token, sender, message):
    pass

def payment_arrived(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Payment Received", body=f"Payment arrived"))
    )
    return data

def rent_paid(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Rent Paid", body=f"You have successfully paid your rent!")), additional_registration_ids=[r_token]
    )
    return data

def due_date_arrived(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Due date arrived", body=f"Pay your rent in time!")), additional_registration_ids=[r_token]
    )
    return data

# LANDLORD
def withdrawal_request_approved(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Withdrawal request", body=f"Your payment request has been approved!"))
    )
    return data


def withdrawal_request_denied(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Withdrawal request", body=f"Your payment request has been denied!")), additional_registration_ids=[r_token]
    )
    return data

def new_message_arrived(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="New Message", body=f"You have a new unread message")), additional_registration_ids=[r_token]
    )
    return data

def application_approved(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Application", body=f"You have an approved application."))
    )
    return data


def appointment_date_arrived(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Appointment", body=f"Don't forget your appointment today!")), additional_registration_ids=[r_token]
    )
    return data


def account_verified(r_token, user=None):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    data = data.send_message(
        Message(notification=Notification(title="Hello", body=f"Your account has been verified!")), additional_registration_ids=[r_token]
    )
    return data


def appointment_approved(r_token, property, date):
    if r_token.lower() == "__empty__":
        return
    data, _ = FCMDevice.objects.get_or_create(registration_id=r_token, type="android")
    from datetime import datetime
    data = data.send_message(
        Message(notification=Notification(title="Appointment", body=f"Your appointment for {property} on {date.strftime('%A %B %d, %Y %I:%M %p')} has been approved."))
    )
    return data
