import pytest
from django.contrib.auth.models import Group, Permission
from django.test.client import Client
from trucks.models import PaymentMethod

from .factories import PaymentMethodFactory

GROUP = "owners"
MODELS = ["Truck", "Image", "location"]
PERMISSIONS = ["add", "change", "delete", "view"]


@pytest.fixture()
def base_setup(db):
    PaymentMethodFactory(payment_name="Cash")
    PaymentMethodFactory(payment_name="Credit Card")
    PaymentMethodFactory(payment_name="Debit Card")
    PaymentMethodFactory(payment_name="By phone")
    new_group, created = Group.objects.get_or_create(name="Owners")
    for model in MODELS:
        for permission in PERMISSIONS:
            name = f"Can {permission} {model}"
            model_add_perm = Permission.objects.get(name=name)
            new_group.permissions.add(model_add_perm)
    assert PaymentMethod.objects.count() == 4
    assert new_group.permissions.count() == 12


@pytest.fixture
def basic_user(db, django_user_model, django_username_field):
    user = UserFactory(
        username="basic_user",
        password=make_password("secret"),
        is_active=True,
        is_staff=False,
        is_superuser=False,
    )
    return user


@pytest.fixture()
def basic_user_client(db, basic_user):
    client = Client()
    client.login(username=basic_user.username, password="secret")
    return client


@pytest.fixture()
def owner_user_client(db, basic_user):
    owner_group = Group.objects.get(name="Owners")
    my_group.user_set.add(basic_user)
    client = Client()
    client.login(username=basic_user.username, password="secret")
    return client
