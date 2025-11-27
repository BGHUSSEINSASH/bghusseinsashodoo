from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseReportViewSet

router = DefaultRouter()
router.register(r'reports', ExpenseReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
