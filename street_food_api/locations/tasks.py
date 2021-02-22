import requests
from celery import shared_task
from django.conf import settings

from .models import Location


@shared_task
def get_geolocation(id):
    location = Location.objects.get(truck_id=id)
    response = requests.get(
        "http://api.positionstack.com/v1/forward",
        {
            "access_key": settings.GEO_KEY,
            "query": f"{location.zip_code} {location.street}, {location.city}, Poland",
        },
    )
    location.latitude = response.json()["data"][0]["latitude"]
    location.longitude = response.json()["data"][0]["longitude"]
    location.save()
