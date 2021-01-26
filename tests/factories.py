import factory
from django.contrib.auth import get_user_model
from factory.faker import faker
from trucks.models import PaymentMethod, Truck

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
