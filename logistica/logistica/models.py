from django.db import models

class CentroAcopio(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.TextField()
    direccion = models.CharField(max_length=255, default="")
    telefono = models.CharField(max_length=50, default="")
    encargado = models.CharField(max_length=100, default="")
    capacidadTotal = models.IntegerField()
    capacidadUsada = models.IntegerField()
    estado = models.CharField(max_length=50)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):   
    CATEGORIAS = [
        ('ALIMENTOS', 'Alimentos'),
        ('ROPA', 'Ropa y Abrigo'),
        ('MEDICOS', 'Insumos Médicos'),
        ('HIGIENE', 'Higiene'),
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    descripcion = models.TextField(blank=True, null=True)
    unidadMedida = models.CharField(max_length=20, default="unidades")
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    centro = models.ForeignKey(CentroAcopio, on_delete=models.CASCADE)
    cantidad = models.FloatField()
    fechaActualizacion = models.DateTimeField(auto_now=True)