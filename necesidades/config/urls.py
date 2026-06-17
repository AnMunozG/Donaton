from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_necesidades.views import NecesidadViewSet

router = DefaultRouter()
router.register(r'necesidades', NecesidadViewSet, basename='necesidad')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]