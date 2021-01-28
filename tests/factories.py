import factory
from django.contrib.auth import get_user_model
from factory.faker import faker
from trucks.models import PaymentMethod, Truck, TruckImage

FAKE = faker.Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user-%d" % n)
    password = "password"


class TruckFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Truck

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: "Truck-%d" % n)
    description = factory.Faker("text")


class PaymentMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentMethod

    payment_name = factory.Sequence(lambda n: "payment-%d" % n)


class TruckImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TruckImage

    truck = factory.SubFactory(TruckFactory)


small_gif = (
    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    b"\x02\x4c\x01\x00\x3b"
)
