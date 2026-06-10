from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea datos iniciales (migraciones ya cargan todo)"
    def handle(self, *args, **options):
        self.stdout.write("Seed data se carga via migraciones")
