from rest_framework import serializers
from .models import Donacion, ItemDonacion, EstadoDonacion


class ItemDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDonacion
        fields = ['id', 'tipo', 'cantidad', 'unidad', 'detalles']


class DonacionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='idDonacion', read_only=True)
    items = ItemDonacionSerializer(many=True, read_only=True)
    estado = serializers.SlugRelatedField(slug_field='nombre', queryset=EstadoDonacion.objects.all())

    class Meta:
        model = Donacion
        fields = ['id', 'tipo', 'cantidad', 'unidad', 'origen', 'centroId',
                  'fecha', 'estado', 'detalles', 'items', 'created_at', 'updated_at']
        extra_kwargs = {
            'tipo': {'required': False, 'allow_null': True},
            'cantidad': {'required': False, 'allow_null': True},
            'unidad': {'required': False, 'allow_null': True},
        }
