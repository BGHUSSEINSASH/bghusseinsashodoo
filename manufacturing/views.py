from rest_framework import viewsets
from .models import WorkOrder
from .serializers import WorkOrderSerializer


class WorkOrderViewSet(viewsets.ModelViewSet):
	queryset = WorkOrder.objects.all().order_by('-start_date')
	serializer_class = WorkOrderSerializer
