from django.db import migrations, models
import django.db.models.deletion


ESTADOS_MAP = {
    "En acopio": "Donación Registrada",
    "Recibido": "Donación Registrada",
    "En tránsito": "En transporte",
    "Entregado": "Recibida",
}


def seed_estados(apps, schema_editor):
    EstadoDonacion = apps.get_model("api_donaciones", "EstadoDonacion")
    for nombre in ["Donación Registrada", "En Recolección", "En transporte", "Recibida"]:
        EstadoDonacion.objects.get_or_create(nombre=nombre)


def migrate_estados_forward(apps, schema_editor):
    Donacion = apps.get_model("api_donaciones", "Donacion")
    EstadoDonacion = apps.get_model("api_donaciones", "EstadoDonacion")
    for d in Donacion.objects.all():
        nuevo = ESTADOS_MAP.get(d.estado, d.estado)
        estado_obj, _ = EstadoDonacion.objects.get_or_create(nombre=nuevo)
        d.estado_fk = estado_obj
        d.save(update_fields=["estado_fk"])


def migrate_estados_reverse(apps, schema_editor):
    Donacion = apps.get_model("api_donaciones", "Donacion")
    for d in Donacion.objects.all():
        if d.estado_fk:
            d.estado = d.estado_fk.nombre
            d.save(update_fields=["estado"])


class Migration(migrations.Migration):
    dependencies = [
        ("api_donaciones", "0004_seed_data"),
    ]

    operations = [
        migrations.CreateModel(
            name="EstadoDonacion",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "verbose_name": "Estado de donación",
                "verbose_name_plural": "Estados de donación",
                "ordering": ["id"],
            },
        ),
        migrations.RunPython(seed_estados),
        migrations.AddField(
            model_name="donacion",
            name="estado_fk",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="api_donaciones.EstadoDonacion"),
        ),
        migrations.RunPython(migrate_estados_forward, migrate_estados_reverse),
        migrations.RemoveField(
            model_name="donacion",
            name="estado",
        ),
        migrations.RenameField(
            model_name="donacion",
            old_name="estado_fk",
            new_name="estado",
        ),
        migrations.AlterField(
            model_name="donacion",
            name="estado",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="api_donaciones.EstadoDonacion"),
        ),
    ]
