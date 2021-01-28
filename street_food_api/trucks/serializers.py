from django.conf import settings
from locations.serializers import LocationSerializer
from rest_framework import serializers, validators

from .models import PaymentMethod, Truck, TruckImage


class TruckImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckImage
        fields = ("id", "image")

    def validate_image(self, value):
        if value.size > settings.MAX_IMG_SIZE:
            raise serializers.ValidationError("File size too big!")
        return value


class TruckSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True,)
    owner = serializers.PrimaryKeyRelatedField(read_only=True,)
    name = serializers.CharField(
        max_length=50,
        validators=[
            validators.UniqueValidator(queryset=Truck.confirmed.all())
        ],
    )
    images = serializers.SerializerMethodField()
    payment_methods = serializers.SerializerMethodField()

    class Meta:
        model = Truck
        fields = (
            "id",
            "owner",
            "name",
            "phone",
            "email",
            "facebook",
            "instagram",
            "page_url",
            "description",
            "payment_methods",
            "images",
            "updated",
            "location",
        )

    def _get_payments(self, data):
        new_payments = []
        payments = data.get("payment")
        for payment in payments.split(", "):
            try:
                filtered_payment = PaymentMethod.objects.get(
                    payment_name__iexact=payment
                ).id
            except PaymentMethod.DoesNotExist:
                raise serializers.ValidationError(
                    "Given payment method does not match"
                )
            new_payments.append(filtered_payment)
        return new_payments

    def create(self, validated_data):
        data = self.context.get("view").request.data
        new_payments = data.get("payment", {})
        if new_payments:
            new_payments = self._get_payments(data)
        truck = Truck.objects.create(**validated_data)
        if data.get("image"):
            for image_data in data.getlist("image"):
                TruckImage.objects.create(truck=truck, image=image_data)
        truck.payment_methods.add(*new_payments)
        return truck

    """
    If an image is sent all previous images will be removed and new images will be associated. The same goes for the payment methods in case of PUT method or PATCH when `payment` is provided. When PATCH without `payment` keyword, old `payment` instances remain.
    """

    def update(self, instance, validated_data):
        data = self.context.get("view").request.data
        method = self.context.get("view").request.method
        new_payments = data.get("payment", {})
        if new_payments:
            new_payments = self._get_payments(data)
        if data.get("image"):
            images = instance.images.all()
            if images.exists():
                instance.images.all().delete()
            for image_data in data.getlist("image"):
                TruckImage.objects.create(truck=instance, image=image_data)
        if method == "PUT" or method == "PATCH" and new_payments:
            instance.payment_methods.clear()
        instance.payment_methods.add(*new_payments)
        return super(TruckSerializer, self).update(instance, validated_data)

    def get_images(self, obj):
        images = obj.images.all()
        return [img.image.url for img in images]

    def get_payment_methods(self, obj):
        return obj.payment_methods.values_list("payment_name", flat=True)
