from django.db import migrations, models
import django.db.models.deletion


LOGROS = [
    ("primera_donacion", "Primera Donación", "Realiza tu primera donación", "bi-award-fill", 1),
    ("corazon_solidario", "Corazón Solidario", "Realiza 5 donaciones", "bi-heart-fill", 2),
    ("angel_guardian", "Ángel Guardián", "Realiza 10 donaciones", "bi-stars", 3),
    ("explorador", "Explorador", "Dona a 3 centros distintos", "bi-compass-fill", 4),
    ("donaton_pro", "Donatón Pro", "Dona a 5 centros distintos", "bi-trophy-fill", 5),
    ("peso_pesado", "Peso Pesado", "Dona 100 kg en total", "bi-box-seam-fill", 6),
    ("manos_abiertas", "Manos Abiertas", "Dona 500 kg en total", "bi-gem", 7),
    ("multi_item", "Multi-tarea", "Realiza una donación con 3 o más artículos distintos", "bi-layers-fill", 8),
]


def seed_logros(apps, schema_editor):
    Logro = apps.get_model("api_servicio", "Logro")
    for codigo, nombre, descripcion, icono, orden in LOGROS:
        Logro.objects.get_or_create(
            codigo=codigo,
            defaults={
                "nombre": nombre,
                "descripcion": descripcion,
                "icono": icono,
                "categoria": "general",
                "orden": orden,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("api_servicio", "0003_crear_admin"),
    ]

    operations = [
        migrations.CreateModel(
            name="Logro",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.SlugField(max_length=50, unique=True)),
                ("nombre", models.CharField(max_length=100)),
                ("descripcion", models.TextField(blank=True)),
                ("icono", models.CharField(default="bi-award-fill", max_length=50)),
                ("categoria", models.CharField(blank=True, max_length=50)),
                ("orden", models.IntegerField(default=0)),
            ],
            options={
                "verbose_name": "Logro",
                "verbose_name_plural": "Logros",
                "ordering": ["orden"],
            },
        ),
        migrations.CreateModel(
            name="LogroUsuario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_obtenido", models.DateTimeField(auto_now_add=True)),
                ("progreso", models.FloatField(default=0.0)),
                ("logro", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="api_servicio.logro")),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="logros", to="api_servicio.usuario")),
            ],
            options={
                "verbose_name": "Logro de usuario",
                "verbose_name_plural": "Logros de usuarios",
                "unique_together": {("usuario", "logro")},
            },
        ),
        migrations.RunPython(seed_logros),
    ]
