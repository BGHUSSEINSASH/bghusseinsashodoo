"""
URL configuration for bgh_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from website.views import homepage
from xmlrpc_server import xmlrpc_endpoint
from api_views import api_documentation, api_health_check, system_info

urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('xmlrpc/2/', xmlrpc_endpoint, name='xmlrpc'),
    path('api/docs/', api_documentation, name='api_docs'),
    path('api/health/', api_health_check, name='api_health'),
    path('api/info/', system_info, name='system_info'),
    path('api/core/', include('core.urls')),
    path('api/accounting/', include('accounting.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/purchases/', include('purchases.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/hr/', include('hr.urls')),
    path('api/projects/', include('project_management.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('api/website/', include('website.urls')),
    path('api/pos/', include('pos.urls')),
    path('api/manufacturing/', include('manufacturing.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/fleet/', include('fleet.urls')),
    path('api/quality/', include('quality.urls')),
    path('api/helpdesk/', include('helpdesk.urls')),
    path('api/events/', include('events.urls')),
    path('api/elearning/', include('elearning.urls')),
    path('api/recruitment/', include('recruitment.urls')),
    path('api/sign/', include('sign.urls')),
    path('api/email/', include('email_marketing.urls')),
    path('api/surveys/', include('surveys.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/discuss/', include('discuss.urls')),
]
