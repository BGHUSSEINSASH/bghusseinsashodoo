from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QualityCheckViewSet

router = DefaultRouter()
router.register(r'checks', QualityCheckViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
