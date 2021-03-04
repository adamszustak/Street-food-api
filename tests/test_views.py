import datetime
from unittest.mock import patch

import pytest
from django.contrib.auth.models import Group
from freezegun import freeze_time
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from locations.models import Location
from trucks.models import PaymentMethod, Truck
from trucks.serializers import TruckSerializer

from .factories import LocationFactory, TruckFactory


@pytest.mark.django_db
def test_viewset_trucklist_GET(basic_user_client):
    trucks = TruckFactory.create_batch(3, is_confirmed=True)
    TruckFactory.create_batch(3, is_confirmed=False)
    url = reverse("v1:truck-list")

    # anonymous
    response = APIClient().get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        "Authentication credentials were not provided."
        in response.data["detail"]
    )

    # logged
    response = basic_user_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(trucks) == response.data["count"]
    for index, truck in enumerate(trucks):
        truck_dict = TruckSerializer(instance=truck).data
        response_dict = dict((response.data)["results"][index])
        truck_dict.pop("payment_methods")
        response_dict.pop("payment_methods")
        assert truck_dict == response_dict


@pytest.mark.django_db
def test_viewset_trucklist_queries_GET(base_setup, basic_user_client):
    truck_name = TruckFactory(name="Heaven", is_confirmed=True)
    truck_city = TruckFactory(city="Warsaw", is_confirmed=True)
    truck_payment = TruckFactory(is_confirmed=True)
    truck_payment.payment_methods.add(
        PaymentMethod.objects.get(payment_name="Cash")
    )
    assert Truck.objects.count() == 3

    url = reverse("v1:truck-list")
    # name
    response = basic_user_client.get(url, {"name": "heav"})
    truck_dict = TruckSerializer(instance=truck_name).data
    truck_dict.pop("payment_methods")
    response_truck = dict(response.data["results"][0])
    response_truck.pop("payment_methods")
    assert response.status_code == status.HTTP_200_OK
    assert truck_dict == response_truck

    # city
    response = basic_user_client.get(url, {"city": "wars"})
    truck_dict = TruckSerializer(instance=truck_city).data
    truck_dict.pop("payment_methods")
    response_truck = dict(response.data["results"][0])
    response_truck.pop("payment_methods")
    assert response.status_code == status.HTTP_200_OK
    assert truck_dict == response_truck

    # payment
    response = basic_user_client.get(url, {"payment": "cash"})
    truck_dict = TruckSerializer(instance=truck_payment).data
    truck_dict.pop("payment_methods")
    response_truck = dict(response.data["results"][0])
    response_truck.pop("payment_methods")
    assert response.status_code == status.HTTP_200_OK
    assert truck_dict == response_truck

    # wrong queries
    response = basic_user_client.get(
        url, {"payment": "ca", "city": "szcz", "name": "uga"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert not response.data["results"]


@pytest.mark.django_db
def test_viewset_truckdetail_GET(basic_user_client):
    truck = TruckFactory(is_confirmed=True)
    url = reverse("v1:truck-detail", args=[truck.id])

    # anonymous
    response = APIClient().get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        "Authentication credentials were not provided."
        in response.data["detail"]
    )

    # logged
    response = basic_user_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    truck_dict = TruckSerializer(instance=truck).data
    truck_dict.pop("payment_methods")
    response.data.pop("payment_methods")
    assert truck_dict == response.data


@pytest.mark.django_db
def test_viewset_trucklist_POST(basic_user_client, owner_user_client):
    data = {
        "name": "Odyssey",
        "description": "Yeah",
        "city": "Warsaw",
        "page_url": "https://www.uczsieit.pl",
    }
    url = reverse("v1:truck-list")

    # anonymous
    response = APIClient().post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        "Authentication credentials were not provided."
        in response.data["detail"]
    )

    # logged without perm
    response = basic_user_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        "You do not have permission to perform this action."
        in response.data["detail"]
    )

    # logged with perm
    response = owner_user_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Truck.objects.count() == 1
    for k, v in data.items():
        assert v in getattr(Truck.objects.latest("id"), k)
        assert v in response.data[k]


@pytest.mark.django_db
def test_viewset_truckdetail_PUT(
    basic_user_client, basic_user, owner_user_client, owner_user
):
    truck = TruckFactory(owner=owner_user, is_confirmed=True)
    data = {"name": "Odyssey", "description": "Yeah", "city": "Warsaw"}
    url = reverse("v1:truck-detail", args=[truck.id])

    # not owner
    owner_group = Group.objects.get(name="Owners")
    owner_group.user_set.add(basic_user)
    response = basic_user_client.put(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        "You do not have permission to perform this action."
        in response.data["detail"]
    )

    # owner
    response = owner_user_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    for k, v in data.items():
        assert v in getattr(Truck.objects.latest("id"), k)
        assert v in response.data[k]


@pytest.mark.django_db
def test_viewset_truckdetail_DELETE(
    basic_user_client, basic_user, owner_user_client, owner_user
):
    truck = TruckFactory(owner=owner_user, is_confirmed=True)
    url = reverse("v1:truck-detail", args=[truck.id])

    # not owner
    owner_group = Group.objects.get(name="Owners")
    owner_group.user_set.add(basic_user)
    response = basic_user_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        "You do not have permission to perform this action."
        in response.data["detail"]
    )

    # owner
    response = owner_user_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Truck.objects.filter(id=truck.id).exists()


@patch("locations.tasks.get_geolocation.delay")
@pytest.mark.django_db(transaction=True)
def test_viewset_truckdetail_LOCATION_POST(
    mocked_task, basic_user_client, basic_user, owner_user_client, owner_user
):
    truck = TruckFactory(owner=owner_user, is_confirmed=True)
    data = {"street": "Mazowiecka 12", "zip_code": "03-111"}
    url = reverse("v1:truck-location", args=[truck.id])

    # not owner
    owner_group = Group.objects.get(name="Owners")
    owner_group.user_set.add(basic_user)
    response = basic_user_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        "You do not have permission to perform this action."
        in response.data["detail"]
    )

    # owner
    response = owner_user_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Location.objects.count() == 1
    for k, v in data.items():
        assert v in getattr(Location.objects.latest("id"), k)
        assert v in response.data[k]
    mocked_task.assert_called_with(truck.id)


@pytest.mark.django_db
def test_viewset_trucklist_MINE_GET(
    basic_user_client, basic_user, owner_user_client, owner_user
):
    truck = TruckFactory(owner=owner_user, is_confirmed=True)
    owner_group = Group.objects.get(name="Owners")
    owner_group.user_set.add(basic_user)
    url = reverse("v1:truck-mine")

    # owner
    response = owner_user_client.get(url)
    truck_dict = TruckSerializer(instance=truck).data
    truck_dict.pop("payment_methods")
    response_truck = dict(response.data["results"][0])
    response_truck.pop("payment_methods")
    assert response.status_code == status.HTTP_200_OK
    assert truck_dict == response_truck

    # not owner
    response = basic_user_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert not response.data["results"]


@pytest.mark.django_db
def test_viewset_trucklist_OPENS_GET(basic_user_client, basic_user):
    truck_open = TruckFactory(name="Truczek", is_confirmed=True)
    truck_closed = TruckFactory(is_confirmed=True)
    LocationFactory(
        truck=truck_open,
        open_from=datetime.time(6),
        closed_at=datetime.time(18),
    )
    LocationFactory(
        truck=truck_closed,
        open_from=datetime.time(10),
        closed_at=datetime.time(16),
    )
    url = reverse("v1:truck-opens")

    # both open
    freezer = freeze_time("2021-02-02 12:00:01")
    freezer.start()
    response = basic_user_client.get(url)
    freezer.stop()
    assert response.data["count"] == 2

    # one open
    freezer = freeze_time("2021-02-02 07:00:01")
    freezer.start()
    response = basic_user_client.get(url)
    freezer.stop()
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == truck_open.name

    # both closed
    freezer = freeze_time("2021-02-02 04:00:01")
    freezer.start()
    response = basic_user_client.get(url)
    freezer.stop()
    assert response.data["count"] == 0
