from rest_framework import serializers
from .models import ExpenseReport


class ExpenseReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseReport
        fields = '__all__'
