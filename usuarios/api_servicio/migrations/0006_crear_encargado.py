from django.db import migrations


def crear_encargado(apps, schema_editor):
    Usuario = apps.get_model('api_servicio', 'Usuario')
    rut = '222222222'
    if not Usuario.objects.filter(rut=rut).exists():
        Usuario.objects.create_user(
            rut=rut,
            username=rut,
            first_name='Encargado',
            last_name='Centro',
            email='encargado@donaton.cl',
            password='admin1234',
            is_staff=False,
            is_superuser=False,
            centro_acopio_id='1',
        )


def eliminar_encargado(apps, schema_editor):
    Usuario = apps.get_model('api_servicio', 'Usuario')
    Usuario.objects.filter(rut='222222222').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api_servicio', '0005_usuario_centro_acopio_id'),
    ]

    operations = [
        migrations.RunPython(crear_encargado, eliminar_encargado),
    ]
