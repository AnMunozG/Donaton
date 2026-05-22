from django.db import migrations


def crear_admin(apps, schema_editor):
    Usuario = apps.get_model('api_servicio', 'Usuario')
    if not Usuario.objects.filter(rut='11111111-1').exists():
        Usuario.objects.create_user(
            rut='11111111-1',
            username='11111111-1',
            first_name='Usuario',
            last_name='1',
            email='admin@donaton.cl',
            password='admin1234',
            is_staff=True,
            is_superuser=True,
        )


class Migration(migrations.Migration):
    dependencies = [
        ('api_servicio', '0002_alter_usuario_groups_alter_usuario_rut_and_more'),
    ]
    operations = [
        migrations.RunPython(crear_admin),
    ]
