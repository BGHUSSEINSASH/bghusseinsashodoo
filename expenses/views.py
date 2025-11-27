from rest_framework import viewsets
from .models import ExpenseReport
from .serializers import ExpenseReportSerializer


class ExpenseReportViewSet(viewsets.ModelViewSet):
    queryset = ExpenseReport.objects.all().order_by('-date')
    serializer_class = ExpenseReportSerializer
