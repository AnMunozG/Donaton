from django.core.management.base import BaseCommand
from api_donaciones.models import Donacion


class Command(BaseCommand):
    help = "Siembra datos de ejemplo para donaciones"

    def handle(self, *args, **options):
        if Donacion.objects.exists():
            self.stdout.write("Ya existen donaciones, se omite seed.")
            return

        datos = [
            {"tipo": "Alimentos no perecibles", "cantidad": 500, "unidad": "kg", "origen": "Donante Anónimo", "centroId": "1", "fecha": "2026-06-01", "estado": "Recibido"},
            {"tipo": "Ropa y abrigo", "cantidad": 10, "unidad": "cajas", "origen": "Empresa Solidaria S.A.", "centroId": "2", "fecha": "2026-06-02", "estado": "Pendiente"},
            {"tipo": "Insumos médicos", "cantidad": 200, "unidad": "unidades", "origen": "Farmashop", "centroId": "3", "fecha": "2026-06-03", "estado": "Recibido"},
            {"tipo": "Donación Monetaria", "cantidad": 1000000, "unidad": "CLP", "origen": "Maria Gonzalez", "centroId": "1", "fecha": "2026-06-04", "estado": "Recibido"},
        ]
        for d in datos:
            Donacion.objects.create(**d)
        self.stdout.write(self.style.SUCCESS("Seed de donaciones completado: 4 donaciones creadas."))
