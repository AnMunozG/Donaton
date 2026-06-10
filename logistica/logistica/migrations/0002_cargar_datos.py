from django.db import migrations

def cargar_centros_completos(apps, schema_editor):
    CentroAcopio = apps.get_model('logistica', 'CentroAcopio')
    CentroAcopio.objects.all().delete()

    centros = [
        {
            "nombre": "Centro de Acopio Santiago Centro",
            "region": "Metropolitana",
            "direccion": "Av. Libertador Bernardo O'Higgins 1234, Santiago",
            "telefono": "+56 9 8765 4321",
            "encargado": "Carolina Méndez",
            "capacidadTotal": 5000,
            "capacidadUsada": 3200,
            "estado": "Activo",
            "latitud": -33.4489,
            "longitud": -70.6693,
            "inventario": [
                {"tipo": "Alimentos", "cantidad": "1.200 kg"},
                {"tipo": "Ropa y abrigo", "cantidad": "8 cajas"},
                {"tipo": "Insumos médicos", "cantidad": "45 unidades"}
            ]
        },
        {
            "nombre": "Centro de Acopio Puente Alto",
            "region": "Metropolitana",
            "direccion": "Calle Los Quillayes 456, Puente Alto",
            "telefono": "+56 9 7654 3210",
            "encargado": "Roberto Soto",
            "capacidadTotal": 3000,
            "capacidadUsada": 2800,
            "estado": "Capacidad crítica",
            "latitud": -33.5929,
            "longitud": -70.5759,
            "inventario": [
                {"tipo": "Alimentos", "cantidad": "900 kg"},
                {"tipo": "Artículos de higiene", "cantidad": "120 unidades"}
            ]
        },
        {
            "nombre": "Centro de Acopio Maipú",
            "region": "Metropolitana",
            "direccion": "Av. Pajaritos 789, Maipú",
            "telefono": "+56 9 6543 2109",
            "encargado": "Valentina Rojas",
            "capacidadTotal": 4000,
            "capacidadUsada": 1500,
            "estado": "Activo",
            "latitud": -33.5000,
            "longitud": -70.8000,
            "inventario": [
                {"tipo": "Ropa y abrigo", "cantidad": "15 cajas"},
                {"tipo": "Utensilios del hogar", "cantidad": "30 unidades"}
            ]
        },
        {
            "nombre": "Centro de Acopio Valparaíso",
            "region": "Valparaíso",
            "direccion": "Av. Argentina 321, Valparaíso",
            "telefono": "+56 9 5432 1098",
            "encargado": "Felipe Araya",
            "capacidadTotal": 3500,
            "capacidadUsada": 700,
            "estado": "Activo",
            "latitud": -33.0472,
            "longitud": -71.6089,
            "inventario": [
                {"tipo": "Alimentos", "cantidad": "300 kg"},
                {"tipo": "Insumos médicos", "cantidad": "18 unidades"}
            ]
        },
        {
            "nombre": "Centro de Acopio Concepción",
            "region": "Biobío",
            "direccion": "Av. Costanera 555, Concepción",
            "telefono": "+56 9 4321 0987",
            "encargado": "Daniela Vergara",
            "capacidadTotal": 4500,
            "capacidadUsada": 1200,
            "estado": "Activo",
            "latitud": -36.8250,
            "longitud": -73.0333,
            "inventario": [
                {"tipo": "Alimentos", "cantidad": "600 kg"},
                {"tipo": "Pañales e infantiles", "cantidad": "200 unidades"}
            ]
        },
        {
            "nombre": "Centro de Acopio La Serena",
            "region": "Coquimbo",
            "direccion": "Av. Juan Bohón 888, La Serena",
            "telefono": "+56 9 3210 9876",
            "encargado": "Mauricio Olivares",
            "capacidadTotal": 3000,
            "capacidadUsada": 1800,
            "estado": "Activo",
            "latitud": -29.9000,
            "longitud": -71.2000,
            "inventario": [
                {"tipo": "Alimentos", "cantidad": "750 kg"},
                {"tipo": "Ropa y abrigo", "cantidad": "12 cajas"},
                {"tipo": "Artículos de higiene", "cantidad": "80 kits"}
            ]
        }
    ]

    for c in centros:
        CentroAcopio.objects.create(**c)

class Migration(migrations.Migration):
    dependencies = [
        ('logistica', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(cargar_centros_completos),
    ]