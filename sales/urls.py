from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesOrderViewSet, QuoteViewSet

router = DefaultRouter()
router.register(r'orders', SalesOrderViewSet)
router.register(r'quotes', QuoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
