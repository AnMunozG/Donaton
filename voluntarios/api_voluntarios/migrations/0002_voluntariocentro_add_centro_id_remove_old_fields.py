import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_voluntarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoluntarioCentro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centro_id', models.CharField(help_text='ID del centro en el microservicio de Logística', max_length=50, verbose_name='ID del centro')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('activo', 'Activo'), ('inactivo', 'Inactivo')], default='pendiente', max_length=20, verbose_name='Estado')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de solicitud')),
                ('voluntario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voluntario_centros', to='api_voluntarios.voluntario', verbose_name='Voluntario')),
            ],
            options={
                'verbose_name': 'Voluntario-Centro',
                'verbose_name_plural': 'Voluntarios-Centros',
                'ordering': ['-fecha_registro'],
                'unique_together': {('voluntario', 'centro_id')},
            },
        ),
        migrations.AddField(
            model_name='registrohoras',
            name='centro_id',
            field=models.CharField(blank=True, default='', help_text='Centro donde se registraron las horas', max_length=50, verbose_name='ID del centro'),
        ),
        migrations.RemoveField(
            model_name='voluntario',
            name='centro_preferido',
        ),
        migrations.RemoveField(
            model_name='voluntario',
            name='estado',
        ),
    ]
