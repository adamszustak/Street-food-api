import requests
from celery.exceptions import MaxRetriesExceededError, SoftTimeLimitExceeded
from django.conf import settings

from conf.celery import app

from .models import Location


@app.task(bind=True, max_retries=3, soft_time_limit=10, default_retry_delay=60)
def get_geolocation(self, id):
    location = Location.objects.get(truck_id=id)
    try:
        url = "http://api.positionstack.com/v1/forward"
        response = requests.get(
            url,
            {
                "access_key": settings.GEO_KEY,
                "query": f"{location.zip_code} {location.street}, {location.city}, Poland",
            },
        )
        latitude = response.json()["data"][0]["latitude"]
        longitude = response.json()["data"][0]["longitude"]
    except (KeyError, SoftTimeLimitExceeded):
        try:
            self.retry()
        except MaxRetriesExceededError:
            pass
    else:
        location.latitude = latitude
        location.longitude = longitude
        location.save()
