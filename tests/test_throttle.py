from unittest.mock import patch

from django.urls import reverse
from rest_framework import status


@patch("rest_framework.throttling.SimpleRateThrottle.get_rate")
def test_throttle_get(mock_throttle, basic_user_client):
    mock_throttle.return_value = "2/hour"
    url = reverse("v1:truck-list")
    response = basic_user_client.get(url)
    headers = response._headers
    assert response.status_code == status.HTTP_200_OK
    assert headers.get("x-rate-limit-limit-get", ())[1] == "2/hour"
    assert headers.get("x-rate-limit-remaining-get", ())[1] == "1"
    assert headers.get("x-rate-limit-reset-get", ())[1] == "60"

    response = basic_user_client.get(url)
    headers = response._headers
    assert response.status_code == status.HTTP_200_OK
    assert headers.get("x-rate-limit-limit-get", ())[1] == "2/hour"
    assert headers.get("x-rate-limit-remaining-get", ())[1] == "0"
    assert headers.get("x-rate-limit-reset-get", ())[1] == "59"

    response = basic_user_client.get(url)
    headers = response._headers
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert headers.get("x-rate-limit-limit-get", ())[1] == "2/hour"
    assert headers.get("x-rate-limit-remaining-get", ())[1] == "0"
    assert headers.get("x-rate-limit-reset-get", ())[1] == "59"


@patch("rest_framework.throttling.SimpleRateThrottle.get_rate")
def test_throttle_post(mock_throttle, owner_user_client):
    mock_throttle.return_value = "1/hour"
    url = reverse("v1:truck-list")
    data = {"name": "Odyssey", "description": "Yeah", "city": "Warsaw"}
    response = owner_user_client.post(url, data)
    headers = response._headers
    assert response.status_code == status.HTTP_201_CREATED
    assert headers.get("x-rate-limit-limit-post", ())[1] == "1/hour"
    assert headers.get("x-rate-limit-remaining-post", ())[1] == "0"
    assert headers.get("x-rate-limit-reset-post", ())[1] == "60"

    response = owner_user_client.post(url, data)
    headers = response._headers
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert headers.get("x-rate-limit-limit-post", ())[1] == "1/hour"
    assert headers.get("x-rate-limit-remaining-post", ())[1] == "0"
    assert headers.get("x-rate-limit-reset-post", ())[1] == "59"
