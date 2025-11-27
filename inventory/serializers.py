from rest_framework import serializers
from .models import StockMove


class StockMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMove
        fields = '__all__'
