from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="Agradecimiento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("centro_id", models.CharField(max_length=50)),
                ("usuario_rut", models.CharField(max_length=12)),
                ("donacion_id", models.CharField(blank=True, max_length=50, null=True)),
                ("mensaje", models.TextField()),
                ("fecha", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Agradecimiento",
                "verbose_name_plural": "Agradecimientos",
            },
        ),
        migrations.CreateModel(
            name="SeguimientoCentro",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("usuario_rut", models.CharField(max_length=12)),
                ("centro_id", models.CharField(max_length=50)),
                ("fecha_inicio", models.DateTimeField(auto_now_add=True)),
                ("activo", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Seguimiento de centro",
                "verbose_name_plural": "Seguimientos de centros",
                "unique_together": {("usuario_rut", "centro_id")},
            },
        ),
    ]
