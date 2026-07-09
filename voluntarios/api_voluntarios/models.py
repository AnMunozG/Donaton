from django.db import models


class Voluntario(models.Model):
    DISPONIBILIDAD_CHOICES = [
        ("diaria", "Diaria"),
        ("semanal", "Semanal"),
        ("fines_semana", "Fines de semana"),
        ("emergencia", "Solo emergencias"),
    ]

    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    disponibilidad = models.CharField(
        max_length=20, choices=DISPONIBILIDAD_CHOICES, default="emergencia"
    )
    habilidades = models.JSONField(default=list, blank=True, verbose_name="Habilidades")
    centro_preferido = models.CharField(
        max_length=50, blank=True, default="",
        verbose_name="Centro de acopio preferido",
        help_text="ID lógico del centro en el microservicio de Logística"
    )
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="pendiente",
        verbose_name="Estado"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Voluntario"
        verbose_name_plural = "Voluntarios"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"Voluntario {self.rut} ({self.get_estado_display()})"

    @property
    def horas_acumuladas(self):
        total = self.registros_horas.aggregate(total=models.Sum("horas"))
        return total["total"] or 0

    @property
    def activo(self):
        return self.estado == "activo"


class RegistroHoras(models.Model):
    voluntario = models.ForeignKey(
        Voluntario, on_delete=models.CASCADE,
        related_name="registros_horas", verbose_name="Voluntario"
    )
    horas = models.PositiveIntegerField(verbose_name="Horas trabajadas")
    descripcion = models.TextField(blank=True, default="", verbose_name="Descripción")
    registrado_por_rut = models.CharField(
        max_length=12, verbose_name="RUT de quien registró"
    )
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del registro")

    class Meta:
        verbose_name = "Registro de horas"
        verbose_name_plural = "Registros de horas"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.horas}h - {self.voluntario.rut} ({self.fecha.date()})"


class AsignacionVoluntario(models.Model):
    ESTADO_CHOICES = [
        ("propuesto", "Propuesto"),
        ("asignado", "Asignado"),
        ("completado", "Completado"),
        ("cancelado", "Cancelado"),
    ]

    voluntario = models.ForeignKey(
        Voluntario, on_delete=models.CASCADE,
        related_name="asignaciones", verbose_name="Voluntario"
    )
    necesidad_id = models.PositiveIntegerField(
        verbose_name="ID de la necesidad",
        help_text="Enlace lógico al microservicio de Necesidades"
    )
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="propuesto"
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asignación de voluntario"
        verbose_name_plural = "Asignaciones de voluntarios"
        ordering = ["-fecha_asignacion"]
        unique_together = ("voluntario", "necesidad_id")

    def __str__(self):
        return f"{self.voluntario.rut} → Necesidad #{self.necesidad_id} ({self.estado})"
