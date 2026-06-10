from django.db import migrations


def actualizar_regiones(apps, schema_editor):
    CentroAcopio = apps.get_model("logistica", "CentroAcopio")
    CentroAcopio.objects.filter(region="Metropolitana").update(region="Metropolitana de Santiago")


class Migration(migrations.Migration):
    dependencies = [
        ("logistica", "0006_hacer_campos_opcionales"),
    ]
    operations = [
        migrations.RunPython(actualizar_regiones),
    ]
