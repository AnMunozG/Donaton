from django.db import migrations
from datetime import datetime


def seed_necesidades(apps, schema_editor):
    Necesidad = apps.get_model('api_necesidades', 'Necesidad')
    now = datetime.now()
    necesidades = [
        {
            "centro_acopio_id": 1,
            "titulo": "Pañales para bebés",
            "descripcion": "Necesitamos pañales talla M y G para bebés de familias damnificadas. Se requieren al menos 500 paquetes.",
            "categoria": "ALIMENTOS",
            "estado": "APROBADA",
            "urgencia": "ALTA",
            "cantidad_requerida": 500,
            "cantidad_recibida": 120,
            "unidad_medida": "paquetes",
            "solicitante_nombre": "1111111111",
            "solicitante_contacto": "admin@donaton.cl",
            "detalles": {},
            "fecha_creacion": now,
            "fecha_actualizacion": now,
        },
        {
            "centro_acopio_id": 2,
            "titulo": "Frazadas y abrigo",
            "descripcion": "Se necesitan frazadas, sacos de dormir y ropa de abrigo para familias en zonas cordilleranas.",
            "categoria": "ROPA",
            "estado": "APROBADA",
            "urgencia": "ALTA",
            "cantidad_requerida": 300,
            "cantidad_recibida": 45,
            "unidad_medida": "unidades",
            "solicitante_nombre": "1111111111",
            "solicitante_contacto": "admin@donaton.cl",
            "detalles": {},
            "fecha_creacion": now,
            "fecha_actualizacion": now,
        },
        {
            "centro_acopio_id": 3,
            "titulo": "Agua embotellada",
            "descripcion": "Urgente: necesidad de agua potable para comunidades sin acceso por cortes de suministro.",
            "categoria": "ALIMENTOS",
            "estado": "APROBADA",
            "urgencia": "ALTA",
            "cantidad_requerida": 1000,
            "cantidad_recibida": 200,
            "unidad_medida": "litros",
            "solicitante_nombre": "1111111111",
            "solicitante_contacto": "admin@donaton.cl",
            "detalles": {},
            "fecha_creacion": now,
            "fecha_actualizacion": now,
        },
        {
            "centro_acopio_id": 1,
            "titulo": "Kit de higiene personal",
            "descripcion": "Solicitamos kits de higiene (jabón, pasta dental, cepillo, toalla) para damnificados.",
            "categoria": "UTILES",
            "estado": "Pendiente",
            "urgencia": "MEDIA",
            "cantidad_requerida": 200,
            "cantidad_recibida": 0,
            "unidad_medida": "kits",
            "solicitante_nombre": "1111111111",
            "solicitante_contacto": "admin@donaton.cl",
            "detalles": {},
            "fecha_creacion": now,
            "fecha_actualizacion": now,
        },
        {
            "centro_acopio_id": 2,
            "titulo": "Insumos médicos básicos",
            "descripcion": "Se requieren vendas, gasas, alcohol gel, guantes quirúrgicos y mascarillas.",
            "categoria": "SALUD",
            "estado": "Cubierto",
            "urgencia": "BAJA",
            "cantidad_requerida": 150,
            "cantidad_recibida": 150,
            "unidad_medida": "unidades",
            "solicitante_nombre": "1111111111",
            "solicitante_contacto": "admin@donaton.cl",
            "detalles": {},
            "fecha_creacion": now,
            "fecha_actualizacion": now,
        },
    ]
    for data in necesidades:
        Necesidad.objects.create(**data)


def remove_seed_necesidades(apps, schema_editor):
    Necesidad = apps.get_model('api_necesidades', 'Necesidad')
    Necesidad.objects.filter(solicitante_nombre="1111111111", titulo__in=[
        "Pañales para bebés", "Frazadas y abrigo", "Agua embotellada",
        "Kit de higiene personal", "Insumos médicos básicos",
    ]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api_necesidades', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_necesidades, remove_seed_necesidades),
    ]
