from rest_framework import serializers

from .models import PaymentMethod, Truck, TruckImage

# class PaymentMethodSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = PaymentMethod
#         fields = '__all__'


# class TruckImageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = TruckImage
#         fields = ('id', 'image')


class TruckSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    payment_methods = serializers.SerializerMethodField()

    class Meta:
        model = Truck
        fields = (
            "id",
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

    def get_images(self, obj):
        images = obj.images.all()
        return [img.image.url for img in images]

    def get_payment_methods(self, obj):
        return obj.payment_methods.values_list("payment_name", flat=True)
