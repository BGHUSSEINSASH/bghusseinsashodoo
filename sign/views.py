from rest_framework import viewsets
from .models import SignatureRequest
from .serializers import SignatureRequestSerializer


class SignatureRequestViewSet(viewsets.ModelViewSet):
    queryset = SignatureRequest.objects.all().order_by('-created_at')
    serializer_class = SignatureRequestSerializer
