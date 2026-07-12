from rest_framework import serializers
from .models import Voluntario, VoluntarioCentro, RegistroHoras, AsignacionVoluntario, Notificacion


class VoluntarioSerializer(serializers.ModelSerializer):
    horas_acumuladas = serializers.ReadOnlyField()

    class Meta:
        model = Voluntario
        fields = [
            "id", "rut", "disponibilidad", "habilidades",
            "fecha_registro", "horas_acumuladas",
        ]
        read_only_fields = ["fecha_registro"]


class VoluntarioCentroSerializer(serializers.ModelSerializer):
    horas_acumuladas = serializers.ReadOnlyField()

    class Meta:
        model = VoluntarioCentro
        fields = ["id", "voluntario", "centro_id", "estado", "fecha_registro", "horas_acumuladas"]
        read_only_fields = ["fecha_registro"]


class RegistroHorasSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroHoras
        fields = ["id", "voluntario", "centro_id", "horas", "descripcion", "registrado_por_rut", "fecha"]
        read_only_fields = ["fecha"]

    def validate_horas(self, value):
        if value <= 0:
            raise serializers.ValidationError("Las horas deben ser mayores a cero.")
        if value > 24:
            raise serializers.ValidationError("No se pueden registrar más de 24 horas en una sola entrada.")
        return value


class AsignacionVoluntarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsignacionVoluntario
        fields = ["id", "voluntario", "necesidad_id", "estado", "fecha_asignacion", "fecha_actualizacion"]
        read_only_fields = ["fecha_asignacion", "fecha_actualizacion"]


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ["id", "voluntario", "titulo", "mensaje", "leida", "enviado_por_rut", "fecha_creacion"]
        read_only_fields = ["fecha_creacion", "leida"]
