from unittest.mock import patch

import pytest
import requests

from locations.tasks import get_geolocation

from .factories import LocationFactory, TruckFactory


@patch.object(requests, "get")
@pytest.mark.django_db
def test_task_get_geolocation(mock_get):
    data = {
        "data": [
            {
                "latitude": 52,
                "longitude": 21,
                "type": "locality",
                "label": "Warsaw, Poland",
            }
        ]
    }
    truck = TruckFactory(is_confirmed=True)
    location = LocationFactory(truck=truck)
    mock_get.return_value.json.return_value = data
    get_geolocation(truck.id)
    location.refresh_from_db()
    assert location.latitude == data["data"][0]["latitude"]
    assert location.longitude == data["data"][0]["longitude"]
