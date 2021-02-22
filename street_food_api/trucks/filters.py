import datetime

from django.db.models import F, Q
from django_filters import rest_framework as filters

from .models import Truck


class TruckFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    payment = filters.CharFilter(
        field_name="payment_methods__payment_name",
        lookup_expr="iexact",
    )

    class Meta:
        model = Truck
        fields = ["name", "city", "payment"]
