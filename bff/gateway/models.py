from django.db import models


class SeguimientoCentro(models.Model):
    usuario_rut = models.CharField(max_length=12)
    centro_id = models.CharField(max_length=50)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ("usuario_rut", "centro_id")
        verbose_name = "Seguimiento de centro"
        verbose_name_plural = "Seguimientos de centros"

    def __str__(self):
        return f"{self.usuario_rut} → {self.centro_id}"


class Agradecimiento(models.Model):
    centro_id = models.CharField(max_length=50)
    usuario_rut = models.CharField(max_length=12)
    donacion_id = models.CharField(max_length=50, null=True, blank=True)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agradecimiento"
        verbose_name_plural = "Agradecimientos"

    def __str__(self):
        return f"{self.centro_id} → {self.usuario_rut}: {self.mensaje[:50]}"
