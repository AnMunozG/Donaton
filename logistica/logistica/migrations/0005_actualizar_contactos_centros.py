from django.db import migrations


def actualizar_contactos(apps, schema_editor):
    CentroAcopio = apps.get_model('logistica', 'CentroAcopio')

    contactos = {
        1: {"direccion": "Av. Libertador Bernardo O'Higgins 1234, Santiago", "telefono": "+56 9 1234 5678", "encargado": "María González"},
        2: {"direccion": "Av. Concha y Toro 2345, Puente Alto", "telefono": "+56 9 2345 6789", "encargado": "Carlos Muñoz"},
        3: {"direccion": "Av. Pajaritos 3456, Maipú", "telefono": "+56 9 3456 7890", "encargado": "Ana Soto"},
        4: {"direccion": "Calle Prat 4567, Valparaíso", "telefono": "+56 9 4567 8901", "encargado": "Pedro Vargas"},
        5: {"direccion": "Av. Pedro de Valdivia 5678, Concepción", "telefono": "+56 9 5678 9012", "encargado": "Laura Rojas"},
        6: {"direccion": "Av. del Mar 6789, La Serena", "telefono": "+56 9 6789 0123", "encargado": "Jorge López"},
    }

    for pk, datos in contactos.items():
        CentroAcopio.objects.filter(pk=pk).update(**datos)

    CentroAcopio.objects.filter(pk__gt=6).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('logistica', '0004_centroacopio_direccion_encargado_telefono'),
    ]

    operations = [
        migrations.RunPython(actualizar_contactos),
    ]
