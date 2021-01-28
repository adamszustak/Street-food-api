import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from .factories import TruckFactory, TruckImageFactory, small_gif


@pytest.mark.django_db
def test_image_directory_path():
    truck = TruckFactory(name="Truczek")
    image = SimpleUploadedFile(
        name="test_image.jpg", content=small_gif, content_type="image/jpeg"
    )
    truck_image = TruckImageFactory(truck=truck, image=image)
    assert (
        f"/media/uploads/{truck.name}/main/{image.name}"
        == truck_image.image.url[:-12] + ".jpg"
    )


@pytest.mark.django_db
def test_generate_slug():
    truck = TruckFactory(name="Truczek")
    assert truck.slug == "truczek"

    truck1 = TruckFactory(name="Truczek")
    assert truck1.slug == "truczek-1"

    truck2 = TruckFactory(name="Truczek-1")
    assert truck2.slug == "truczek-1-1"
