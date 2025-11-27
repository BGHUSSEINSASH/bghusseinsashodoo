from rest_framework import viewsets
from .models import StockMove
from .serializers import StockMoveSerializer


class StockMoveViewSet(viewsets.ModelViewSet):
	queryset = StockMove.objects.all().order_by('-date')
	serializer_class = StockMoveSerializer
