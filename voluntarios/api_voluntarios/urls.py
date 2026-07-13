from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VoluntarioViewSet, VoluntarioCentroViewSet, AsignacionVoluntarioViewSet, NotificacionViewSet

router = DefaultRouter()
router.register(r"voluntarios", VoluntarioViewSet, basename="voluntario")
router.register(r"voluntario-centros", VoluntarioCentroViewSet, basename="voluntariocentro")
router.register(r"asignaciones", AsignacionVoluntarioViewSet, basename="asignacion")
router.register(r"notificaciones", NotificacionViewSet, basename="notificacion")

urlpatterns = [
    path("", include(router.urls)),
]
