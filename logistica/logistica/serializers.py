from rest_framework import serializers
from .models import CentroAcopio, EstadoCentro

class CentroAcopioSerializer(serializers.ModelSerializer):
    estado = serializers.SlugRelatedField(slug_field='nombre', queryset=EstadoCentro.objects.all())

    class Meta:
        model = CentroAcopio
        fields = ['idCentro', 'nombre', 'region', 'direccion', 
                  'telefono', 'encargado', 'capacidadTotal', 'capacidadUsada', 
                  'estado', 'latitud', 'longitud', 'inventario']
