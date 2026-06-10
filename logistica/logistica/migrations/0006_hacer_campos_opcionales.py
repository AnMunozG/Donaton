# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logistica", "0005_actualizar_contactos_centros"),
    ]

    operations = [
        migrations.AlterField(
            model_name="centroacopio",
            name="direccion",
            field=models.CharField(default="", max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name="centroacopio",
            name="telefono",
            field=models.CharField(default="", max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name="centroacopio",
            name="encargado",
            field=models.CharField(default="", max_length=100, blank=True),
        ),
    ]
