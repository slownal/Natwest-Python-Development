from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, ReportConfigViewSet, api_root

router = DefaultRouter()
router.register(r'reports', ReportViewSet)
router.register(r'configs', ReportConfigViewSet)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
] 