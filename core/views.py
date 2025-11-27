from rest_framework import viewsets
from .models import Customer, Supplier, Warehouse, Product, Employee
from .serializers import (
	CustomerSerializer,
	SupplierSerializer,
	WarehouseSerializer,
	ProductSerializer,
	EmployeeSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all().order_by('-created_at')
	serializer_class = CustomerSerializer


class SupplierViewSet(viewsets.ModelViewSet):
	queryset = Supplier.objects.all().order_by('-created_at')
	serializer_class = SupplierSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
	queryset = Warehouse.objects.all().order_by('name')
	serializer_class = WarehouseSerializer


class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all().order_by('sku')
	serializer_class = ProductSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
	queryset = Employee.objects.all().order_by('last_name')
	serializer_class = EmployeeSerializer
