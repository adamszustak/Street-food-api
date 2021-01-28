from unittest.mock import Mock

import pytest
from django.conf import settings
from django.http import QueryDict
from locations.serializers import LocationSerializer
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from trucks.models import PaymentMethod, Truck, TruckImage
from trucks.serializers import TruckImageSerializer, TruckSerializer

from .factories import TruckFactory, UserFactory, small_gif


@pytest.mark.django_db
def test_unique_validation_truckserializer():
    TruckFactory(name="HamBug", is_confirmed=True)
    truck_serializer = TruckSerializer(
        data={"name": "HamBug", "description": "Desc"}
    )
    assert not truck_serializer.is_valid()
    assert "This field must be unique." in truck_serializer.errors["name"]
    assert Truck.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payment", ["casssh", "debit card, credit c", "debbit carrd, cash"]
)
def test_payments_validation_truckserializer_fail(base_setup, payment):
    # create
    data = {"name": "HamBug", "description": "Desc"}
    mock_view = Mock()
    mock_view.request = APIRequestFactory().request()
    mock_view.request.data = {"payment": payment}
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
    data = {"name": "HamBug", "description": "Desc"}
    mock_view = Mock()
    mock_view.request = APIRequestFactory().request()
    mock_view.request.user = UserFactory()
    mock_view.request.data = {"payment": payment}
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
    data = {"name": "HamBug", "description": "Desc"}
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
