from unittest.mock import Mock

import pytest
from django.conf import settings
from django.http import QueryDict
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from locations.models import Location
from locations.serializers import LocationSerializer
from trucks.models import PaymentMethod, Truck, TruckImage
from trucks.serializers import TruckImageSerializer, TruckSerializer

from .factories import TruckFactory, UserFactory, small_gif


@pytest.mark.django_db
def test_unique_validation_truckserializer():
    TruckFactory(name="HamBug", is_confirmed=True)
    truck_serializer = TruckSerializer(
        data={"name": "HamBug", "description": "Desc", "city": "Warsaw"}
    )
    assert not truck_serializer.is_valid()
    assert "This field must be unique." in truck_serializer.errors["name"]
    assert Truck.objects.count() == 1


@pytest.mark.parametrize(
    "payment", ["casssh", "debit card, credit c", "debbit carrd, cash"]
)
def test_payments_validation_truckserializer_fail(base_setup, payment):
    # create
    data = {"name": "HamBug", "description": "Desc", "city": "Warsaw"}
    mock_view = Mock()
    mock_view.request = APIRequestFactory().request()
    mock_view.request.data = {"payment_methods": payment}
    mock_view.request.user = UserFactory()
    serializer = TruckSerializer(data=data, context={"view": mock_view})
    serializer.is_valid()
    with pytest.raises(serializers.ValidationError):
        serializer.save()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payment", ["cash", "debit card, credit card, cash, by phone", ""]
)
def test_payments_validation_truckserializer_pass(base_setup, payment):
    # create
    data = {"name": "HamBug", "description": "Desc", "city": "Warsaw"}
    mock_view = Mock()
    mock_view.request = APIRequestFactory().request()
    mock_view.request.user = UserFactory()
    mock_view.request.data = {"payment_methods": payment}
    serializer = TruckSerializer(data=data, context={"view": mock_view})
    serializer.is_valid()
    serializer.save(owner=mock_view.request.user)
    truck = Truck.objects.filter(name=serializer.data["name"])
    assert truck.exists()

    # update
    mock_view.request.method = "POST"
    serializer = TruckSerializer(
        truck[0], data=data, context={"view": mock_view}
    )
    serializer.is_valid()
    serializer.save()
    for p in list(
        truck[0].payment_methods.values_list("payment_name", flat=True)
    ):
        assert p.lower() in payment.split(", ")

    mock_view.request.method = "PATCH"
    serializer = TruckSerializer(
        truck[0], data=data, context={"view": mock_view}
    )
    serializer.is_valid()
    serializer.save()
    for p in list(
        truck[0].payment_methods.values_list("payment_name", flat=True)
    ):
        assert p.lower() in payment.split(", ")

    mock_view.request.method = "PATCH"
    mock_view.request.data = {}
    serializer = TruckSerializer(
        truck[0], data=data, context={"view": mock_view}
    )
    serializer.is_valid()
    serializer.save()
    for p in list(
        truck[0].payment_methods.values_list("payment_name", flat=True)
    ):
        assert p.lower() in payment.split(", ")


@pytest.mark.django_db
def test_image_saving_truckserializer():
    # create
    data = {"name": "HamBug", "description": "Desc", "city": "Warsaw"}
    mock_view = Mock()
    mock_view.request = APIRequestFactory().request()
    mock_view.request.user = UserFactory()
    mock_view.request.data = QueryDict(f"image={small_gif}&image={small_gif}")
    serializer = TruckSerializer(data=data, context={"view": mock_view})
    serializer.is_valid()
    serializer.save(owner=mock_view.request.user)
    truck = Truck.objects.get(name=serializer.data["name"])
    assert truck.images.exists()
    assert TruckImage.objects.filter(truck=truck).count() == 2

    # update
    mock_view.request.data = QueryDict(f"image={small_gif}")
    serializer = TruckSerializer(truck, data=data, context={"view": mock_view})
    serializer.is_valid()
    serializer.save()
    truck = Truck.objects.get(name=serializer.data["name"])
    assert truck.images.exists()
    assert TruckImage.objects.filter(truck=truck).count() == 1


@pytest.mark.parametrize("zip_code", ["03", "03-44", "ala", "O3-444"])
def test_zipcode_validation_locationserializer_fail(zip_code):
    data = {"street": "Mazowiecka", "zip_code": zip_code}
    serializer = LocationSerializer(data=data)
    serializer.is_valid()
    assert "Wrong zip code entered" in serializer.errors["zip_code"]


@pytest.mark.parametrize("zip_code", ["03-441", "00-000", "99-999"])
def test_zipcode_validation_locationserializer_pass(zip_code):
    data = {"street": "Mazowiecka", "zip_code": zip_code}
    serializer = LocationSerializer(data=data)
    serializer.is_valid()
    assert not serializer.errors


@pytest.mark.parametrize(
    "latitude, longitude", [(+90.1, -100.111), (-91, 180), (75, 181)]
)
def test_coordinates_validation_locationserializer_fail(latitude, longitude):
    data = {
        "street": "Mazowiecka",
        "zip_code": "03-411",
        "longitude": longitude,
        "latitude": latitude,
    }
    serializer = LocationSerializer(data=data)
    serializer.is_valid()
    assert (
        "Wrong latitude or longitude entered"
        in serializer.errors["non_field_errors"]
    )


@pytest.mark.parametrize(
    "latitude, longitude",
    [
        (45, 180),
        (+90.0, -127.554334),
        (-90.000, -180.0000),
        (+90, +180),
        (47.1231231, 179.99999999),
    ],
)
def test_coordinates_validation_locationserializer_pass(latitude, longitude):
    data = {
        "street": "Mazowiecka",
        "zip_code": "03-411",
        "longitude": longitude,
        "latitude": latitude,
    }
    serializer = LocationSerializer(data=data)
    serializer.is_valid()
    assert not serializer.errors


@pytest.mark.django_db
def test_location_saving_locationserializer(db):
    # create
    truck = TruckFactory()
    data = {"street": "Mazowiecka", "zip_code": "03-411"}
    serializer = LocationSerializer(data=data)
    serializer.is_valid()
    serializer.save(truck=truck)
    assert Location.objects.filter(truck=truck.id).exists()

    # update
    data = {"street": "Mazowiecka", "zip_code": "03-444"}
    serializer = LocationSerializer(data=data)
    serializer.is_valid()
    serializer.save(truck=truck)
    location = Location.objects.filter(truck=truck.id)
    assert location.count() == 1
    assert location[0].zip_code == "03-444"
