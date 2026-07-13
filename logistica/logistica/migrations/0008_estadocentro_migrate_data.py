from django.db import migrations, models
import django.db.models.deletion


ESTADOS_MAP = {
    "Activo": "Activo",
    "Normal": "Activo",
    "Capacidad crítica": "Capacidad crítica",
    "Capacidad moderada": "Capacidad crítica",
    "Inactivo": "Inactivo",
}


def seed_estados(apps, schema_editor):
    EstadoCentro = apps.get_model("logistica", "EstadoCentro")
    for nombre in ["Activo", "Capacidad crítica", "Inactivo"]:
        EstadoCentro.objects.get_or_create(nombre=nombre)


def migrate_estados_forward(apps, schema_editor):
    CentroAcopio = apps.get_model("logistica", "CentroAcopio")
    EstadoCentro = apps.get_model("logistica", "EstadoCentro")
    for c in CentroAcopio.objects.all():
        nuevo = ESTADOS_MAP.get(c.estado, "Activo")
        estado_obj, _ = EstadoCentro.objects.get_or_create(nombre=nuevo)
        c.estado_fk = estado_obj
        c.save(update_fields=["estado_fk"])


def migrate_estados_reverse(apps, schema_editor):
    CentroAcopio = apps.get_model("logistica", "CentroAcopio")
    for c in CentroAcopio.objects.all():
        if c.estado_fk:
            c.estado = c.estado_fk.nombre
            c.save(update_fields=["estado"])


class Migration(migrations.Migration):
    dependencies = [
        ("logistica", "0007_actualizar_regiones_seed"),
    ]

    operations = [
        migrations.CreateModel(
            name="EstadoCentro",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name": "Estado de centro",
                "verbose_name_plural": "Estados de centro",
                "ordering": ["id"],
            },
        ),
        migrations.RunPython(seed_estados),
        migrations.AddField(
            model_name="centroacopio",
            name="estado_fk",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="logistica.EstadoCentro"),
        ),
        migrations.RunPython(migrate_estados_forward, migrate_estados_reverse),
        migrations.RemoveField(
            model_name="centroacopio",
            name="estado",
        ),
        migrations.RenameField(
            model_name="centroacopio",
            old_name="estado_fk",
            new_name="estado",
        ),
        migrations.AlterField(
            model_name="centroacopio",
            name="estado",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="logistica.EstadoCentro"),
        ),
    ]
