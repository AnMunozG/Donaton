from rest_framework import serializers
from .models import Necesidad

class NecesidadSerializer(serializers.ModelSerializer):
    # Campo calculado dinámicamente que se expone en la API JSON
    porcentaje_progreso = serializers.ReadOnlyField(source='porcentaje_cubierto')

    class Meta:
        model = Necesidad
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'estado', 'cantidad_recibida']

    # --- Validaciones de Negocio ---
    def validate_centro_acopio_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("El ID del centro de acopio debe ser un identificador válido.")
        return value

    def validate(self, data):
        """Validación cruzada de campos"""
        if data.get('cantidad_requerida', 1) <= 0:
            raise serializers.ValidationError({"cantidad_requerida": "La cantidad requerida debe ser mayor a 0."})
        return data