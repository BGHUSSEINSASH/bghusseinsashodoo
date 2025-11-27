from rest_framework import viewsets
from .models import Attendance, Payroll
from .serializers import AttendanceSerializer, PayrollSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
	queryset = Attendance.objects.all().order_by('-date')
	serializer_class = AttendanceSerializer


class PayrollViewSet(viewsets.ModelViewSet):
	queryset = Payroll.objects.all().order_by('-period')
	serializer_class = PayrollSerializer
