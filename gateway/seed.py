"""
Script para poblar la base de datos con cuentas iniciales (auth local del BFF).
Uso: python manage.py shell < gateway/seed.py
"""
import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from gateway.models import Cuenta
from django.contrib.auth.hashers import make_password


def seed():
    print("Poblando cuentas (auth local del BFF)...")

    cuentas_data = [
        {"rut": "111111111", "nombre": "Admin Donatón", "email": "admin@donaton.cl", "rol": "admin", "password": "admin1234"},
        {"rut": "222222222", "nombre": "Usuario Ejemplo", "email": "usuario@donaton.cl", "rol": "donante", "password": "user1234"},
        {"rut": "11.111.111-1", "nombre": "Admin Donatón", "email": "admin2@donaton.cl", "rol": "admin", "password": "admin123"},
        {"rut": "22.222.222-2", "nombre": "María García", "email": "maria@mail.cl", "rol": "donante", "password": "pass123"},
        {"rut": "33.333.333-3", "nombre": "Juan Pérez", "email": "juan@mail.cl", "rol": "beneficiario", "password": "pass123"},
        {"rut": "44.444.444-4", "nombre": "Centro Esperanza", "email": "esperanza@mail.cl", "rol": "beneficiario", "password": "pass123"},
        {"rut": "55.555.555-5", "nombre": "Voluntario Pedro", "email": "pedro@mail.cl", "rol": "voluntario", "password": "pass123"},
    ]
    for data in cuentas_data:
        obj, created = Cuenta.objects.get_or_create(
            rut=data["rut"],
            defaults={
                "nombre": data["nombre"],
                "email": data["email"],
                "rol": data["rol"],
                "password": make_password(data["password"]),
            },
        )
        if created:
            print(f"  Cuenta creada: {obj.nombre} ({obj.rut})")

    print("¡Cuentas pobladas exitosamente!")


if __name__ == "__main__":
    seed()
