from django.conf import settings
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
        )

    def create(self, validated_data):
        data = self.context.get("view").request.data
        truck = Truck.objects.create(**validated_data)
        if data.get("image"):
            for image_data in data.getlist("image"):
                TruckImage.objects.create(truck=truck, image=image_data)
        if data.get("payment"):
            new_payments = []
            payments = data.get("payment")
            for payment in payments.split(", "):
                filtered_payment = PaymentMethod.objects.get(
                    payment_name__iexact=payment
                ).id
                new_payments.append(filtered_payment)
            truck.payment_methods.add(*new_payments)
        return truck

    """
    If an image is sent all previous images will be removed and new images will be associated. The same goes for the payment methods.
    """

    def update(self, instance, validated_data):
        data = self.context.get("view").request.data
        if data.get("image"):
            images = instance.images.all()
            if images.exists():
                instance.images.all().delete()
            for image_data in data.getlist("image"):
                TruckImage.objects.create(truck=instance, image=image_data)
        if data.get("payment"):
            new_payments = []
            payments = data.get("payment")
            for payment in payments.split(", "):
                filtered_payment = PaymentMethod.objects.get(
                    payment_name__iexact=payment
                ).id
                new_payments.append(filtered_payment)
            instance.payment_methods.clear()
            instance.payment_methods.add(*new_payments)
        return super(TruckSerializer, self).update(instance, validated_data)

    def get_images(self, obj):
        images = obj.images.all()
        return [img.image.url for img in images]

    def get_payment_methods(self, obj):
        return obj.payment_methods.values_list("payment_name", flat=True)
