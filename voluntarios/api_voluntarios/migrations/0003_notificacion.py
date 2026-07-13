from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api_voluntarios", "0002_voluntariocentro_add_centro_id_remove_old_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notificacion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("titulo", models.CharField(max_length=200, verbose_name="Título")),
                ("mensaje", models.TextField(verbose_name="Mensaje")),
                ("leida", models.BooleanField(default=False, verbose_name="Leída")),
                ("enviado_por_rut", models.CharField(blank=True, default="", max_length=12, verbose_name="RUT de quien envió")),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("voluntario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notificaciones", to="api_voluntarios.voluntario", verbose_name="Voluntario")),
            ],
            options={
                "verbose_name": "Notificación",
                "verbose_name_plural": "Notificaciones",
                "ordering": ["-fecha_creacion"],
            },
        ),
    ]
