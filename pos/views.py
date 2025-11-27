from rest_framework import viewsets
from .models import POSOrder
from .serializers import POSOrderSerializer


class POSOrderViewSet(viewsets.ModelViewSet):
	queryset = POSOrder.objects.all().order_by('-date')
	serializer_class = POSOrderSerializer
