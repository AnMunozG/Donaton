from django.db import migrations, models
import django.db.models.deletion


ESTADOS_MAP = {
    "PENDIENTE": "Pendiente",
    "Pendiente": "Pendiente",
    "APROBADA": "Activa",
    "EN_PROCESO": "Activa",
    "Activa": "Activa",
    "CUBIERTA": "Cubierta",
    "Cubierto": "Cubierta",
    "RECHAZADA": "Cubierta",
}


def seed_estados(apps, schema_editor):
    EstadoNecesidad = apps.get_model("api_necesidades", "EstadoNecesidad")
    for nombre in ["Pendiente", "Activa", "Cubierta"]:
        EstadoNecesidad.objects.get_or_create(nombre=nombre)


def migrate_estados_forward(apps, schema_editor):
    Necesidad = apps.get_model("api_necesidades", "Necesidad")
    EstadoNecesidad = apps.get_model("api_necesidades", "EstadoNecesidad")
    for n in Necesidad.objects.all():
        nuevo = ESTADOS_MAP.get(n.estado, "Pendiente")
        estado_obj, _ = EstadoNecesidad.objects.get_or_create(nombre=nuevo)
        n.estado_fk = estado_obj
        n.save(update_fields=["estado_fk"])


def migrate_estados_reverse(apps, schema_editor):
    Necesidad = apps.get_model("api_necesidades", "Necesidad")
    for n in Necesidad.objects.all():
        if n.estado_fk:
            n.estado = n.estado_fk.nombre
            n.save(update_fields=["estado"])


class Migration(migrations.Migration):
    dependencies = [
        ("api_necesidades", "0002_seed_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="EstadoNecesidad",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name": "Estado de necesidad",
                "verbose_name_plural": "Estados de necesidad",
                "ordering": ["id"],
            },
        ),
        migrations.RunPython(seed_estados),
        migrations.AddField(
            model_name="necesidad",
            name="estado_fk",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="api_necesidades.EstadoNecesidad"),
        ),
        migrations.RunPython(migrate_estados_forward, migrate_estados_reverse),
        migrations.RemoveField(
            model_name="necesidad",
            name="estado",
        ),
        migrations.RenameField(
            model_name="necesidad",
            old_name="estado_fk",
            new_name="estado",
        ),
        migrations.AlterField(
            model_name="necesidad",
            name="estado",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="api_necesidades.EstadoNecesidad"),
        ),
    ]
