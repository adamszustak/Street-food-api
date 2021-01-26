import pytest
from locations.serializers import LocationSerializer
from trucks.models import Truck
from trucks.serializers import TruckSerializer

from .factories import TruckFactory


@pytest.mark.django_db
def test_unique_validation_truckserializer(base_setup):
    TruckFactory(name="HamBug", is_confirmed=True)
    truck_serializer = TruckSerializer(
        data={"name": "HamBug", "description": "Desc"}
    )
    assert not truck_serializer.is_valid()
    assert "This field must be unique." in truck_serializer.errors["name"]
    assert Truck.objects.count() == 1
