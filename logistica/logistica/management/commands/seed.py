from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from logistica.models import CentroAcopio


class Command(BaseCommand):
    help = "Crea datos iniciales para Logistica"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            id=1, defaults={
                "username": "system",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            user.set_unusable_password()
            user.save()
            self.stdout.write(self.style.SUCCESS("System user created (id=1)"))
        else:
            self.stdout.write("System user already exists")

        if not CentroAcopio.objects.exists():
            CentroAcopio.objects.create(
                nombre="Centro de Acopio Santiago Centro",
                region="Metropolitana",
                direccion="Av. Libertador Bernardo O'Higgins 1234",
                telefono="+56 2 2345 6789",
                encargado="Carolina Mendez",
                capacidadTotal=5000,
                capacidadUsada=0,
                estado="Activo",
                latitud=-33.4569,
                longitud=-70.6483,
            )
            self.stdout.write(self.style.SUCCESS("Sample centro created"))
        else:
            self.stdout.write("Centros already exist")
