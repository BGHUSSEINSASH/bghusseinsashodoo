from rest_framework import viewsets
from .models import EmailCampaign
from .serializers import EmailCampaignSerializer


class EmailCampaignViewSet(viewsets.ModelViewSet):
    queryset = EmailCampaign.objects.all().order_by('-sent_date')
    serializer_class = EmailCampaignSerializer
