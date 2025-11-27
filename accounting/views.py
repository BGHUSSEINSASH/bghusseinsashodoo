from rest_framework import viewsets
from .models import Invoice, Expense
from .serializers import InvoiceSerializer, ExpenseSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
	queryset = Invoice.objects.all().order_by('-date')
	serializer_class = InvoiceSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
	queryset = Expense.objects.all().order_by('-date')
	serializer_class = ExpenseSerializer
