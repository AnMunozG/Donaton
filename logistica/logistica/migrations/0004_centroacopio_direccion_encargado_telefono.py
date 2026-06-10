from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistica', '0003_crear_system_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='centroacopio',
            name='direccion',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='centroacopio',
            name='encargado',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='centroacopio',
            name='telefono',
            field=models.CharField(default='', max_length=50),
        ),
    ]
