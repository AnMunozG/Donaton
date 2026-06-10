from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CentroAcopioViewSet

router = DefaultRouter()
router.register(r'centros', CentroAcopioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]