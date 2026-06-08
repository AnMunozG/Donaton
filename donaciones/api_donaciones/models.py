from django.db import models

class Donacion(models.Model):
    idDonacion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    unidad = models.CharField(max_length=20, default="kg")
    origen = models.CharField(max_length=150)
    centroId = models.CharField(max_length=50)
    fecha = models.DateField()
    estado = models.CharField(max_length=50)
    detalles = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.id_donacion} - {self.tipo}"
