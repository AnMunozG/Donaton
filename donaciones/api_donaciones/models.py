from django.db import models


class EstadoDonacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado de donación"
        verbose_name_plural = "Estados de donación"
        ordering = ["id"]

    def __str__(self):
        return self.nombre


class Donacion(models.Model):
    idDonacion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=100, null=True, blank=True)
    cantidad = models.IntegerField(null=True, blank=True)
    unidad = models.CharField(max_length=20, default="kg", null=True, blank=True)
    origen = models.CharField(max_length=150)
    centroId = models.CharField(max_length=50)
    fecha = models.DateField()
    estado = models.ForeignKey(EstadoDonacion, on_delete=models.PROTECT)
    detalles = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.idDonacion} - {self.tipo or '(multi-item)'}"


class ItemDonacion(models.Model):
    id = models.AutoField(primary_key=True)
    donacion = models.ForeignKey(Donacion, on_delete=models.CASCADE, related_name='items')
    tipo = models.CharField(max_length=100)
    cantidad = models.FloatField()
    unidad = models.CharField(max_length=20, default="kg")
    detalles = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.tipo} x{self.cantidad}"
