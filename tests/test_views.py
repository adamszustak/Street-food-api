import pytest
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from locations.models import Location
from trucks.models import Truck
from trucks.serializers import TruckSerializer

from .factories import TruckFactory


@pytest.mark.django_db
def test_viewset_trucklist_GET(basic_user_client):
    trucks = TruckFactory.create_batch(3, is_confirmed=True)
    TruckFactory.create_batch(3, is_confirmed=False)
    url = reverse("api:truck-list")

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
def test_viewset_truckdetail_GET(basic_user_client):
    truck = TruckFactory(is_confirmed=True)
    url = reverse("api:truck-detail", args=[truck.id])

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
    url = reverse("api:truck-list")

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
    url = reverse("api:truck-detail", args=[truck.id])

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
    url = reverse("api:truck-detail", args=[truck.id])

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


@pytest.mark.django_db
def test_viewset_truckdetail_LOCATION_POST(
    basic_user_client, basic_user, owner_user_client, owner_user
):
    truck = TruckFactory(owner=owner_user, is_confirmed=True)
    data = {"street": "Mazowiecka 12", "zip_code": "03-111"}
    url = reverse("api:truck-location", args=[truck.id])

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
