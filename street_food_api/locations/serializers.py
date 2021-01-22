from django.conf import settings
from rest_framework import serializers, validators

from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("id", "truck")
        extra_kwargs = {
            "truck": {"required": False},
            "city": {"required": False},
        }
