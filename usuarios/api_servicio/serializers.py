import re
from rest_framework import serializers
from .models import Usuario, Logro, LogroUsuario
from itertools import cycle

class RegistroSerializer(serializers.ModelSerializer):
    # Definimos campos obligatorios y limpios para Swagger
    password = serializers.CharField(write_only=True, required=True)
    rut = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'rut', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'centro_acopio_id']

    def validate_rut(self, value):
        # Tu lógica de validación está perfecta, la mantenemos
        rut_limpio = str(value).upper().replace("-", "").replace(".", "").strip()
        
        if not re.match(r"^\d{7,8}[0-9K]$", rut_limpio):
            raise serializers.ValidationError("RUT inválido: Solo números y K final.")

        cuerpo = rut_limpio[:-1]
        dv_ingresado = rut_limpio[-1]
        reverso = map(int, reversed(cuerpo))
        factores = cycle(range(2, 8))
        suma = sum(d * f for d, f in zip(reverso, factores))
        dv_esperado = str(11 - suma % 11)
        
        if dv_esperado == "11": dv_esperado = "0"
        if dv_esperado == "10": dv_esperado = "K"

        if dv_ingresado != dv_esperado:
            raise serializers.ValidationError("Dígito verificador incorrecto.")

        qs = Usuario.objects.filter(username=rut_limpio)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Este RUT ya está registrado.")
        
        return rut_limpio

    def create(self, validated_data):
        validated_data['username'] = validated_data['rut']
        return Usuario.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        if 'rut' in validated_data:
            validated_data['username'] = validated_data['rut']
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LogroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logro
        fields = ["id", "codigo", "nombre", "descripcion", "icono", "categoria", "orden"]


class LogroUsuarioSerializer(serializers.ModelSerializer):
    logro = LogroSerializer(read_only=True)
    codigo = serializers.SlugField(source="logro.codigo", read_only=True)

    class Meta:
        model = LogroUsuario
        fields = ["id", "logro", "codigo", "fecha_obtenido", "progreso"]