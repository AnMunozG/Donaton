from django.core.management.base import BaseCommand
from api_donaciones.models import Donacion, EstadoDonacion


class Command(BaseCommand):
    help = "Siembra datos de ejemplo para donaciones"

    def handle(self, *args, **options):
        if Donacion.objects.exists():
            self.stdout.write("Ya existen donaciones, se omite seed.")
            return

        # 'estado' es un ForeignKey a EstadoDonacion: no se puede asignar un
        # string plano (eso es justamente lo que rompía el seed con un error
        # de "se esperaba un valor numérico pero llegó un string"). Hay que
        # resolver primero la instancia con get_or_create.
        datos = [
            {"tipo": "Alimentos no perecibles", "cantidad": 500, "unidad": "kg", "origen": "Donante Anónimo", "centroId": "1", "fecha": "2026-06-01", "estado": "Donación Registrada"},
            {"tipo": "Ropa y abrigo", "cantidad": 10, "unidad": "cajas", "origen": "Empresa Solidaria S.A.", "centroId": "2", "fecha": "2026-06-02", "estado": "En Recolección"},
            {"tipo": "Insumos médicos", "cantidad": 200, "unidad": "unidades", "origen": "Farmashop", "centroId": "3", "fecha": "2026-06-03", "estado": "En transporte"},
            {"tipo": "Donación Monetaria", "cantidad": 1000000, "unidad": "CLP", "origen": "Maria Gonzalez", "centroId": "1", "fecha": "2026-06-04", "estado": "Recibida"},
        ]

        creadas = 0
        for d in datos:
            estado_nombre = d.pop("estado")
            estado_obj, _ = EstadoDonacion.objects.get_or_create(nombre=estado_nombre)
            Donacion.objects.create(estado=estado_obj, **d)
            creadas += 1

        self.stdout.write(self.style.SUCCESS(f"Seed de donaciones completado: {creadas} donaciones creadas."))