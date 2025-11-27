from rest_framework import viewsets
from .models import QualityCheck
from .serializers import QualityCheckSerializer


class QualityCheckViewSet(viewsets.ModelViewSet):
    queryset = QualityCheck.objects.all().order_by('-date')
    serializer_class = QualityCheckSerializer
