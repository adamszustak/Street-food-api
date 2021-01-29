import re

from django.conf import settings
from rest_framework import serializers, validators

from trucks.models import Truck

from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("id", "truck")
        extra_kwargs = {
            "truck": {"required": False},
            "city": {"required": False},
            "open_from": {"format": "%H:%M"},
            "closed_at": {"format": "%H:%M"},
        }

    def validate_zip_code(self, value):
        match_zip_code = re.match(r"^\d{2}-\d{3}$", value)
        if not match_zip_code:
            raise serializers.ValidationError("Wrong zip code entered")
        return value

    def validate(self, data):
        if data.get("longitude") or data.get("latitude"):
            coordinates = (
                f"{data.get('latitude', None)}, {data.get('longitude', None)}"
            )
            match_coordinates = re.match(
                r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$",
                coordinates,
            )
            if not match_coordinates:
                raise serializers.ValidationError(
                    "Wrong latitude or longitude entered"
                )
        return data

    def create(self, validated_data):
        truck = validated_data.get("truck", None)
        if Location.objects.filter(truck=truck.id).exists():
            truck.location.delete()
        location = Location.objects.create(**validated_data)
        return location
