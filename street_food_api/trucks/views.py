from rest_framework import response, viewsets

from .models import Truck
from .serializers import TruckSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.confirmed.all()
    serializer_class = TruckSerializer
