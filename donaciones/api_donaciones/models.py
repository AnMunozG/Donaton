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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.idDonacion} - {self.tipo}"
