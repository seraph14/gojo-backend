from django_filters import rest_framework as filters
from transactions.models import Transaction
from django.db.models import Q
from properties.models import Property
from transactions.models import UserRentedProperties
from django.db.models import Avg


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
        # rating = float(value)
        # # TODO: average rating
        # properties = (
        #     queryset.annotate(avg_rating=Avg("reviews__rating")).filter(
        #         avg_rating__gte=rating
        #     )
        #     # queryset.exclude(reviews__rating__lte=rating)
        #     # .distinct("id")
        # )
        return queryset

    class Meta:
        model = Property
        fields = ["q", "categories", "facilities", "minPrice", "maxPrice", "rating"]
