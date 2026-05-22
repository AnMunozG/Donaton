from django.db import migrations
from django.contrib.auth.hashers import make_password


def crear_system_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(id=1).exists():
        User.objects.create(
            id=1,
            username='system',
            is_staff=True,
            is_superuser=True,
            password=make_password('system1234'),
        )


class Migration(migrations.Migration):
    dependencies = [
        ('logistica', '0002_carga_datos'),
    ]
    operations = [
        migrations.RunPython(crear_system_user),
    ]
