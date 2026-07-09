from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoluntarioViewSet, AsignacionVoluntarioViewSet

router = DefaultRouter()
router.register(r"voluntarios", VoluntarioViewSet, basename="voluntario")
router.register(r"asignaciones", AsignacionVoluntarioViewSet, basename="asignacion")

urlpatterns = [
    path("", include(router.urls)),
]
