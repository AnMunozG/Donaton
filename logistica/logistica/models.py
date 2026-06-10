from django.db import models

class CentroAcopio(models.Model):
    idCentro = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, default="", blank=True)
    telefono = models.CharField(max_length=50, default="", blank=True)
    encargado = models.CharField(max_length=100, default="", blank=True)
    capacidadTotal = models.IntegerField()
    capacidadUsada = models.IntegerField()
    estado = models.CharField(max_length=50)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    inventario = models.JSONField(default=list)

    def __str__(self):
        return f"{self.idCentro} -{self.nombre}"
