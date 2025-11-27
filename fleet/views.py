from rest_framework import viewsets
from .models import Vehicle
from .serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('plate_number')
    serializer_class = VehicleSerializer
