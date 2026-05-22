from rest_framework import serializers
from .models import Producto, CentroAcopio, Inventario

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class CentroAcopioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroAcopio
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    productoNombre = serializers.ReadOnlyField(source='producto.nombre')
    centroNombre = serializers.ReadOnlyField(source='centro.nombre')

    class Meta:
        model = Inventario
        fields = ['id', 'centro', 'centroNombre', 'producto', 'productoNombre', 'cantidad']