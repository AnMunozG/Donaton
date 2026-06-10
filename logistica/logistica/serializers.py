from rest_framework import serializers
from .models import CentroAcopio

class CentroAcopioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroAcopio
        fields = ['idCentro', 'nombre', 'region', 'direccion', 
                  'telefono', 'encargado', 'capacidadTotal', 'capacidadUsada', 
                  'estado', 'latitud', 'longitud', 'inventario']
