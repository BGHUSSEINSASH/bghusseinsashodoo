from rest_framework import viewsets
from .models import SalesOrder, Quote
from .serializers import SalesOrderSerializer, QuoteSerializer


class SalesOrderViewSet(viewsets.ModelViewSet):
	queryset = SalesOrder.objects.all().order_by('-date')
	serializer_class = SalesOrderSerializer


class QuoteViewSet(viewsets.ModelViewSet):
	queryset = Quote.objects.all().order_by('-date')
	serializer_class = QuoteSerializer
