from django_filters import rest_framework as filters
from transactions.models import Transaction
from django.db.models import Q
from properties.models import Property
from transactions.models import UserRentedProperties

# class PropertyFilter(filters.FilterSet):
#     status = filters.ChoiceFilter(
#         choices=[(choice[1], choice[0]) for choice in TRANSACTION_STATUS.choices],
#         method="filter_status",
#     )

#     def filter_status(self, queryset, name, value):
#         valid_choices = {
#             choice[1].lower(): choice[0] for choice in TRANSACTION_STATUS.choices
#         }
#         status_value = valid_choices.get(value.lower(), None)
#         if status_value is not None:
#             return queryset.filter(status=status_value)
#         return queryset.none()

#     class Meta:
#         model = Transaction
#         fields = ["status"]


class PropertyFilter(filters.FilterSet):
    q = filters.CharFilter(field_name="title", lookup_expr="icontains")
    categories = filters.CharFilter(method="filter_by_categories")
    facilities = filters.CharFilter(method="filter_by_facilities")
    minPrice = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    maxPrice = filters.NumberFilter(field_name="amount", lookup_expr="lte")
    rating = filters.CharFilter(method="filter_by_rating")

    def filter_by_categories(self, queryset, name, value):
        categories = [int(id) for id in value.split(",")]
        return queryset.filter(category__id__in=categories)

    def filter_by_facilities(self, queryset, name, value):
        facilities = [int(id) for id in value.split(",")]
        return queryset.filter(facilities__id__in=facilities)

    def filter_by_rating(self, queryset, name, value):
        rating = float(value)
        properties = (
            Property.objects.annotate(avg_rating=Avg("reviews__rating"))
            .filter(avg_rating__gte=rating)
            .order_by("avg_rating")
        )
        return properties

    class Meta:
        model = Property
        fields = ["q", "categories", "facilities", "minPrice", "maxPrice", "rating"]
