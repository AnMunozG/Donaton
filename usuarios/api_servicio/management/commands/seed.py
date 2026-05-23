from django.core.management.base import BaseCommand
from api_servicio.models import Usuario


class Command(BaseCommand):
    help = "Crea datos iniciales para Usuarios"

    def handle(self, *args, **options):
        if Usuario.objects.exists():
            self.stdout.write("Users already exist")
            return

        Usuario.objects.create_user(
            rut="111111111",
            username="admin",
            first_name="Admin",
            last_name="",
            email="admin@donaton.cl",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write(self.style.SUCCESS("Admin user created (111111111 / admin123)"))
