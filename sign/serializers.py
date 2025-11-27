from rest_framework import serializers
from .models import SignatureRequest


class SignatureRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignatureRequest
        fields = '__all__'
