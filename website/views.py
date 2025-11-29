from rest_framework import viewsets
from django.shortcuts import render
from .models import Page
from .serializers import PageSerializer


class PageViewSet(viewsets.ModelViewSet):
	queryset = Page.objects.all().order_by('slug')
	serializer_class = PageSerializer


def homepage(request):
	return render(request, 'base.html')
