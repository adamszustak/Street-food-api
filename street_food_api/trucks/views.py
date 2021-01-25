from django.contrib.auth import get_user_model
from locations.serializers import LocationSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import PaymentMethod, Truck
from .permissions import IsOwnerOrReadOnly
from .serializers import TruckImageSerializer, TruckSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.confirmed.all()
    serializer_class = TruckSerializer
    permission_classes = (
        permissions.DjangoModelPermissions,
        IsOwnerOrReadOnly,
    )

    def _get_images(self, request):
        for img in request.data.getlist("image"):
            image_serializer = TruckImageSerializer(data={"image": img})
            image_serializer.is_valid(raise_exception=True)

    def create(self, request, *args, **kwargs):
        if request.data.get("image"):
            self._get_images(request)
        return super(TruckViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        if request.data.get("image"):
            self._get_images(request)
        return super(TruckViewSet, self).update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def location(self, request, pk=None):
        truck = self.get_object()
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(city=truck.city, truck=truck)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
