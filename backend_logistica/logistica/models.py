from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class CentroAcopio(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    capacidad_maxima = models.PositiveIntegerField(help_text="Capacidad total en unidades")
    
    def __str__(self):
        return f"{self.nombre} - {self.comuna}"

class Inventario(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    centro_acopio = models.ForeignKey(CentroAcopio, on_delete=models.CASCADE, related_name='stocks')
    ultima_actualizacion = models.DateTimeField(auto_now=True)