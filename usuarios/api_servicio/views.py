from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
# Eliminamos la importación del Token antiguo
from .models import Usuario
from .serializers import RegistroSerializer

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
            
            # Nota: En JWT, el token no se crea aquí manualmente en la DB.
            # El usuario se registra y luego va al endpoint /api/login/ 
            # para obtener su llave (Access Token).
            
            return Response({
                'mensaje': 'Usuario creado con éxito',
                'rut': user.rut,
                'siguiente_paso': 'Ahora obtén tu token en /api/login/'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)