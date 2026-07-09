from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
# Eliminamos la importación del Token antiguo
from .models import Usuario, Logro, LogroUsuario
from .serializers import RegistroSerializer, LogroSerializer, LogroUsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer

    def get_permissions(self):
        """
        Permite que cualquier persona se registre (POST),
        pero requiere estar logueado para ver la lista (GET, PUT, DELETE).
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'mensaje': 'Usuario creado con éxito',
                'rut': user.rut,
                'siguiente_paso': 'Ahora obtén tu token en /api/login/'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogroViewSet(viewsets.ModelViewSet):
    queryset = Logro.objects.all()
    serializer_class = LogroSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class LogroUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LogroUsuarioSerializer

    def get_queryset(self):
        return LogroUsuario.objects.filter(usuario__rut=self.request.user.rut)

    @action(detail=False, methods=["post"])
    def verificar(self, request):
        """Verifica y otorga logros según las estadísticas enviadas."""
        stats = request.data
        rut = request.user.rut
        usuario = request.user
        logros_obtenidos = []
        logros_usuario = set(LogroUsuario.objects.filter(usuario=usuario).values_list("logro_id", flat=True))

        reglas = [
            ("primera_donacion", "Primera Donación", stats.get("total_donaciones", 0) >= 1),
            ("corazon_solidario", "Corazón Solidario", stats.get("total_donaciones", 0) >= 5),
            ("angel_guardian", "Ángel Guardián", stats.get("total_donaciones", 0) >= 10),
            ("explorador", "Explorador", stats.get("centros_distintos", 0) >= 3),
            ("donaton_pro", "Donatón Pro", stats.get("centros_distintos", 0) >= 5),
            ("peso_pesado", "Peso Pesado", stats.get("total_kg", 0) >= 100),
            ("manos_abiertas", "Manos Abiertas", stats.get("total_kg", 0) >= 500),
            ("multi_item", "Multi-tarea", stats.get("max_items_una_donacion", 0) >= 3),
        ]

        for codigo, nombre, cumple in reglas:
            logro = Logro.objects.filter(codigo=codigo).first()
            if not logro:
                logro = Logro.objects.create(codigo=codigo, nombre=nombre, descripcion=nombre, icono="bi-award-fill", orden=len(reglas))

            if cumple and logro.id not in logros_usuario:
                LogroUsuario.objects.create(usuario=usuario, logro=logro, progreso=100)
                logros_obtenidos.append(codigo)

        return Response({"logros_obtenidos": logros_obtenidos})