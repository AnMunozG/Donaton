import re
from rest_framework import serializers
from .models import Usuario
from itertools import cycle

class RegistroSerializer(serializers.ModelSerializer):
    # Definimos campos obligatorios y limpios para Swagger
    password = serializers.CharField(write_only=True, required=True)
    rut = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'rut', 'email', 'first_name', 'last_name', 'password', 'is_staff']
        extra_kwargs = {'is_staff': {'read_only': True}}

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
        
        return rut_limpio

    def create(self, validated_data):
        # TRUCO PROFESIONAL: 
        # Como Django exige un 'username' internamente, le asignamos el RUT.
        # Así el usuario no tiene que inventar un nombre de usuario.
        validated_data['username'] = validated_data['rut']
        
        # Usamos create_user para que la password se encripte correctamente
        return Usuario.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Si actualizan el RUT, actualizamos el username también
        if 'rut' in validated_data:
            validated_data['username'] = validated_data['rut']
            
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance