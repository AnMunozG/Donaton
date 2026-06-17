from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Necesidad
from .serializers import NecesidadSerializer

class NecesidadViewSet(viewsets.ModelViewSet):
    queryset = Necesidad.objects.all()
    serializer_class = NecesidadSerializer

    def get_queryset(self):
        queryset = Necesidad.objects.all()
        centro_id = self.request.query_params.get('centro_id')
        categoria = self.request.query_params.get('categoria')
        estado = self.request.query_params.get('estado')
        urgencia = self.request.query_params.get('urgencia')

        if centro_id:
            queryset = queryset.filter(centro_acopio_id=centro_id)
        if category := categoria:
            queryset = queryset.filter(categoria=category.upper())
        if estado:
            queryset = queryset.filter(estado=estado)
        if urgencia:
            queryset = queryset.filter(urgencia=urgencia.upper())

        return queryset

    @action(detail=True, methods=['post'], url_path='registrar-donacion')
    def registrar_donacion(self, request, pk=None):
        necesidad = self.get_object()
        cantidad = request.data.get('cantidad', 0)

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                return Response({'error': 'La cantidad a sumar debe ser mayor a cero'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Cantidad no válida'}, status=status.HTTP_400_BAD_REQUEST)

        necesidad.cantidad_recibida += cantidad
        if necesidad.cantidad_recibida >= necesidad.cantidad_requerida:
            necesidad.estado = 'CUBIERTA'
        elif necesidad.cantidad_recibida > 0 and necesidad.estado == 'PENDIENTE':
            necesidad.estado = 'EN_PROCESO'

        necesidad.save()

        serializer = self.get_serializer(necesidad)
        return Response({
            'message': 'Donación registrada e impactada en la necesidad',
            'necesidad': serializer.data
        }, status=status.HTTP_200_OK)