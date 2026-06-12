from rest_framework import serializers
from .models import Donacion

class DonacionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='idDonacion', read_only=True)

    class Meta:
        model = Donacion
        fields = ['id', 'tipo', 'cantidad', 'unidad', 'origen', 'centroId', 'fecha', 'estado', 'detalles']