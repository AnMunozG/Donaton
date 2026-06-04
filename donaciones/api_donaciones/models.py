from django.db import models

class Donacion(models.Model):
    tipo = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    origen = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.tipo} - {self.cantidad} ({self.origen})"
