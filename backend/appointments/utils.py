from django.db import models

class APPOINTMENT_STATUS(models.IntegerChoices):
    PENDING = 0, "pending"
    APPROVED = 1, "approved"
    # FIXME: rejected and cancelled [re think it if a landlord can cancel the appointment after approving it]
    REJECTED = 2, "rejected"
    CANCELED = 3, "canceled"
    PASSED = 4, "passed"