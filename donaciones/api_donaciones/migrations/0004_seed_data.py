from django.db import migrations
from datetime import date


def seed_donaciones(apps, schema_editor):
    Donacion = apps.get_model('api_donaciones', 'Donacion')
    ItemDonacion = apps.get_model('api_donaciones', 'ItemDonacion')
    ahora = date.today()
    donaciones = [
        {
            "tipo": "Alimentos no perecibles",
            "cantidad": 200,
            "unidad": "kg",
            "origen": "1111111111",
            "centroId": "1",
            "fecha": ahora,
            "estado": "Entregado",
            "detalles": {"notas": "Arroz, fideos, legumbres y harina"},
        },
        {
            "tipo": "Ropa y abrigo",
            "cantidad": 80,
            "unidad": "unidades",
            "origen": "1111111111",
            "centroId": "2",
            "fecha": ahora,
            "estado": "En tránsito",
            "detalles": {"notas": "Chaquetas y frazadas nuevas"},
        },
        {
            "tipo": "Donación Monetaria",
            "cantidad": 500000,
            "unidad": "CLP",
            "origen": "1111111111",
            "centroId": "1",
            "fecha": ahora,
            "estado": "Entregado",
            "detalles": {"metodo_pago": "transferencia"},
        },
        {
            "tipo": "Insumos médicos",
            "cantidad": 300,
            "unidad": "unidades",
            "origen": "1111111111",
            "centroId": "3",
            "fecha": ahora,
            "estado": "En acopio",
            "detalles": {"notas": "Mascarillas KN95 y alcohol gel"},
        },
        {
            "tipo": "Artículos de higiene",
            "cantidad": 150,
            "unidad": "kits",
            "origen": "1111111111",
            "centroId": "2",
            "fecha": ahora,
            "estado": "Entregado",
            "detalles": {},
        },
        {
            "tipo": "Donación Monetaria",
            "cantidad": 250000,
            "unidad": "CLP",
            "origen": "1111111111",
            "centroId": "3",
            "fecha": ahora,
            "estado": "Entregado",
            "detalles": {"metodo_pago": "transferencia"},
        },
    ]
    for data in donaciones:
        item = data.pop("detalles", {})
        donacion = Donacion.objects.create(**data)
        if data.get("tipo") != "Donación Monetaria":
            ItemDonacion.objects.create(
                donacion=donacion,
                tipo=data["tipo"],
                cantidad=data["cantidad"],
                unidad=data["unidad"],
                detalles=item,
            )


def remove_seed_donaciones(apps, schema_editor):
    Donacion = apps.get_model('api_donaciones', 'Donacion')
    Donacion.objects.filter(origen="1111111111").delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api_donaciones', '0003_alter_donacion_cantidad_alter_donacion_tipo_and_more'),
    ]
    operations = [
        migrations.RunPython(seed_donaciones, remove_seed_donaciones),
    ]
