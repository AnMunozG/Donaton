from django.db import models


class Voluntario(models.Model):
    DISPONIBILIDAD_CHOICES = [
        ("diaria", "Diaria"),
        ("semanal", "Semanal"),
        ("fines_semana", "Fines de semana"),
        ("emergencia", "Solo emergencias"),
    ]

    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    disponibilidad = models.CharField(
        max_length=20, choices=DISPONIBILIDAD_CHOICES, default="emergencia"
    )
    habilidades = models.JSONField(default=list, blank=True, verbose_name="Habilidades")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Voluntario"
        verbose_name_plural = "Voluntarios"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"Voluntario {self.rut}"

    @property
    def horas_acumuladas(self):
        total = self.registros_horas.aggregate(total=models.Sum("horas"))
        return total["total"] or 0

    @property
    def activo(self):
        return self.voluntario_centros.filter(estado="activo").exists()


class VoluntarioCentro(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    voluntario = models.ForeignKey(
        Voluntario, on_delete=models.CASCADE,
        related_name="voluntario_centros", verbose_name="Voluntario"
    )
    centro_id = models.CharField(
        max_length=50, verbose_name="ID del centro",
        help_text="ID del centro en el microservicio de Logística"
    )
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default="pendiente",
        verbose_name="Estado"
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")

    class Meta:
        verbose_name = "Voluntario-Centro"
        verbose_name_plural = "Voluntarios-Centros"
        unique_together = ("voluntario", "centro_id")
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.voluntario.rut} → Centro {self.centro_id} ({self.estado})"

    @property
    def horas_acumuladas(self):
        total = RegistroHoras.objects.filter(
            voluntario=self.voluntario, centro_id=self.centro_id
        ).aggregate(total=models.Sum("horas"))
        return total["total"] or 0


class RegistroHoras(models.Model):
    voluntario = models.ForeignKey(
        Voluntario, on_delete=models.CASCADE,
        related_name="registros_horas", verbose_name="Voluntario"
    )
    centro_id = models.CharField(
        max_length=50, blank=True, default="",
        verbose_name="ID del centro",
        help_text="Centro donde se registraron las horas"
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


class Notificacion(models.Model):
    voluntario = models.ForeignKey(
        Voluntario, on_delete=models.CASCADE,
        related_name="notificaciones", verbose_name="Voluntario"
    )
    titulo = models.CharField(max_length=200, verbose_name="Título")
    mensaje = models.TextField(verbose_name="Mensaje")
    leida = models.BooleanField(default=False, verbose_name="Leída")
    enviado_por_rut = models.CharField(
        max_length=12, blank=True, default="",
        verbose_name="RUT de quien envió"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.titulo} → {self.voluntario.rut}"
