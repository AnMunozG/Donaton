from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_servicio.views import UsuarioViewSet, LogroViewSet, LogroUsuarioViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'logros', LogroViewSet, basename='logro')
router.register(r'mis-logros', LogroUsuarioViewSet, basename='mis-logro')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
