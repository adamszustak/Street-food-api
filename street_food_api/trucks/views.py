from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import PaymentMethod, Truck
from .serializers import TruckImageSerializer, TruckSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.confirmed.all()
    serializer_class = TruckSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get("image"):
            for img in request.data.getlist("image"):
                image_serializer = TruckImageSerializer(data={"image": img})
                image_serializer.is_valid(raise_exception=True)
        return super(TruckViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=get_user_model().objects.get(id=1))

    def update(self, request, *args, **kwargs):
        if request.data.get("image"):
            for img in request.data.getlist("image"):
                image_serializer = TruckImageSerializer(data={"image": img})
                image_serializer.is_valid(raise_exception=True)
        return super(TruckViewSet, self).update(request, *args, **kwargs)
