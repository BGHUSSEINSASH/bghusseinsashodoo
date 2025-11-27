from rest_framework import serializers
from .models import POSOrder


class POSOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSOrder
        fields = '__all__'
