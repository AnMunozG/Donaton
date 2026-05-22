from django.db import migrations

def cargar_datos_completos_donaton(apps, schema_editor):
    CentroAcopio = apps.get_model('logistica', 'CentroAcopio')

    # --- 1. TODOS LOS CENTROS DE ACOPIO ---
    centros_data = [
        {"nombre": "Centro de Acopio Santiago Centro", "region": "Metropolitana", "capacidadTotal": 5000, "capacidadUsada": 3200, "estado": "Activo", "latitud": -33.4489, "longitud": -70.6693},
        {"nombre": "Centro de Acopio Puente Alto", "region": "Metropolitana", "capacidadTotal": 3000, "capacidadUsada": 2800, "estado": "Capacidad crítica", "latitud": -33.5929, "longitud": -70.5759},
        {"nombre": "Centro de Acopio Maipú", "region": "Metropolitana", "capacidadTotal": 4000, "capacidadUsada": 1500, "estado": "Activo", "latitud": -33.5113, "longitud": -70.7567},
        {"nombre": "Centro de Acopio Valparaíso", "region": "Valparaíso", "capacidadTotal": 3500, "capacidadUsada": 700, "estado": "Activo", "latitud": -33.0458, "longitud": -71.6197},
        {"nombre": "Centro de Acopio Concepción", "region": "Biobío", "capacidadTotal": 4500, "capacidadUsada": 1200, "estado": "Activo", "latitud": -36.8270, "longitud": -73.0503},
        {"nombre": "Centro de Acopio La Serena", "region": "Coquimbo", "capacidadTotal": 3000, "capacidadUsada": 1800, "estado": "Activo", "latitud": -29.9027, "longitud": -71.2520},
    ]
    
    centros_creados = {}
    for c in centros_data:
        obj = CentroAcopio.objects.create(**c)
        centros_creados[c['nombre']] = obj


class Migration(migrations.Migration):
    dependencies = [
        ('logistica', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(cargar_datos_completos_donaton),
    ]