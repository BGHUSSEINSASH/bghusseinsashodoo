from rest_framework import viewsets
from .models import Campaign, Lead
from .serializers import CampaignSerializer, LeadSerializer


class CampaignViewSet(viewsets.ModelViewSet):
	queryset = Campaign.objects.all().order_by('start_date')
	serializer_class = CampaignSerializer


class LeadViewSet(viewsets.ModelViewSet):
	queryset = Lead.objects.all().order_by('name')
	serializer_class = LeadSerializer
