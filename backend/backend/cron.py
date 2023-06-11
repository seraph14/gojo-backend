from datetime import datetime, timedelta
from properties.models import TestModel
from transactions.models import Transaction, UserRentedProperties, PROPERTY_RENT_STATUS
from backend.utilities import due_date_arrived, appointment_date_arrived
from appointments.models import Appointment, APPOINTMENT_STATUS

def notify_and_create_upcoming_transactions():
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=5)

    contracts = UserRentedProperties.objects.filter(
        status=PROPERTY_RENT_STATUS.ONGOING, start_date__range=[current_date, end_date]
    )

    for contract in contracts:
        if contract.users.fb_registration_token != "__empty__":
            due_date_arrived(contract.user.fb_registration_token)
        
        transaction = Transaction.objects.get_or_create(
            sender=contract.user,
            receiver=contract.property.owner,
            amount=contract.property.amount,
            rent_detail=contract,
            payment_date=datetime(
                current_date.year, current_date.month, contract.start_date.day
            ),
        )

def process_upcoming_and_passed_appointment():
    current_date = date.today()
    today_appointments = Appointment.objects.filter(
        appointment_date__year=current_date.year,
        appointment_date__month=current_date.month,
        appointment_date__day=current_date.day,
    )

    for appointment in today_appointments:
        appointment_date_arrived(appointment.tenant.fb_registration_token)
        appointment_date_arrived(appointment.property.owner.fb_registration_token)

    current_date = date.today()

    upcoming_appointments = Appointment.objects.filter(
        appointment_date__date__gt=current_date, status=APPOINTMENT_STATUS.PENDING
    ).update(status=APPOINTMENT_STATUS.PASSED)
