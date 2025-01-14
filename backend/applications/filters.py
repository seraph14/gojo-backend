from django_filters import rest_framework as filters
from applications.models import Application
from applications.utilities import APPLICATION_STATUS


class ApplicationFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=[(choice[1], choice[0]) for choice in APPLICATION_STATUS.choices], method='filter_status')    
    def filter_status(self, queryset, name, value):
        valid_choices = {choice[1].lower(): choice[0] for choice in APPLICATION_STATUS.choices}
        status_value = valid_choices.get(value.lower(), None)
        if status_value is not None:
            return queryset.filter(status=status_value)
        return queryset.none()

    class Meta:
        model = Application
        fields = ["status"] 