from rest_framework import serializers
from .models import Necesidad, EstadoNecesidad

class NecesidadSerializer(serializers.ModelSerializer):
    porcentaje_progreso = serializers.ReadOnlyField(source='porcentaje_cubierto')
    estado = serializers.SlugRelatedField(slug_field='nombre', queryset=EstadoNecesidad.objects.all())

    class Meta:
        model = Necesidad
        fields = [
            'id', 'centro_acopio_id', 'titulo', 'descripcion', 'categoria',
            'estado', 'urgencia', 'cantidad_requerida', 'cantidad_recibida',
            'unidad_medida', 'solicitante_nombre', 'solicitante_contacto',
            'detalles', 'fecha_limite', 'fecha_creacion', 'fecha_actualizacion',
            'porcentaje_progreso',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion', 'cantidad_recibida']

    def validate_centro_acopio_id(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise serializers.ValidationError("El ID del centro de acopio debe ser un identificador válido.")
        return value

    def validate(self, data):
        if data.get('cantidad_requerida', 1) <= 0:
            raise serializers.ValidationError({"cantidad_requerida": "La cantidad requerida debe ser mayor a 0."})
        return data