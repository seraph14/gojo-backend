from django_filters import rest_framework as filters
from appointments.models import Appointment
from appointments.utils import APPOINTMENT_STATUS


class AppointmentFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=[(choice[1], choice[0]) for choice in APPOINTMENT_STATUS.choices], method='filter_status')    
    def filter_status(self, queryset, name, value):
        valid_choices = {choice[1].lower(): choice[0] for choice in APPOINTMENT_STATUS.choices}
        status_value = valid_choices.get(value.lower(), None)
        if status_value is not None:
            return queryset.filter(status=status_value)
        return queryset.none()

    class Meta:
        model = Appointment
        fields = ["status"] 