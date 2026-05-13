from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from decimal import Decimal
from django.db.models import Sum


def generar_code(prefix="", length=6):
    import random, string
    chars = string.ascii_uppercase + string.digits
    return f"{prefix}{''.join(random.choices(chars, k=length))}"


class Cuenta(models.Model):
    ROL_CHOICES = [
        ("donante", "Donante"),
        ("beneficiario", "Beneficiario"),
        ("admin", "Administrador"),
        ("voluntario", "Voluntario"),
    ]

    rut = models.CharField(max_length=12, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="donante")
    telefono = models.CharField(max_length=20, blank=True, default="")
    direccion = models.TextField(blank=True, default="")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        db_table = "cuentas"
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return f"{self.nombre} ({self.rut})"


class Centro(models.Model):
    ESTADO_CHOICES = [
        ("Activo", "Activo"),
        ("Capacidad crítica", "Capacidad crítica"),
        ("Inactivo", "Inactivo"),
    ]

    code = models.CharField(max_length=10, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    region = models.CharField(max_length=50, default="Metropolitana")
    direccion = models.TextField()
    comuna = models.CharField(max_length=50, blank=True, default="")
    telefono = models.CharField(max_length=20, blank=True, default="")
    coordenadas_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    coordenadas_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    capacidad = models.IntegerField(default=0)  # capacidadTotal
    encargado = models.ForeignKey(
        Cuenta, on_delete=models.SET_NULL, null=True, blank=True, related_name="centros"
    )
    # ── Microservicio de Inventario: este campo se poblaría desde el
    #    servicio externo de inventario (inventario-api). Por ahora se
    #    almacena localmente como JSON.
    inventario = models.JSONField(default=list, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Activo")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("CA-")
        super().save(*args, **kwargs)

    @property
    def capacidad_usada(self):
        total = Donacion.objects.filter(
            centro=self, estado__in=["Recibida", "Distribuida", "Entregado"]
        ).aggregate(total=Sum("cantidad"))["total"]
        if self.capacidad > 0 and total:
            return round(float(total) / self.capacidad * 100, 1)
        return 0.0

    class Meta:
        db_table = "centros"
        verbose_name = "Centro de Acopio"
        verbose_name_plural = "Centros de Acopio"

    def __str__(self):
        return f"{self.nombre} ({self.code})"


class TipoRecurso(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default="")
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("TR-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "tipos_recurso"
        verbose_name = "Tipo de Recurso"
        verbose_name_plural = "Tipos de Recurso"

    def __str__(self):
        return self.nombre


class Unidad(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    nombre = models.CharField(max_length=50)
    abreviatura = models.CharField(max_length=10)
    # ── Microservicio de Catálogos: la relación tipo_recurso → unidades
    #    podría venir de un servicio externo de catálogos. Por ahora se
    #    relaciona vía TablaUnidadTipo (abajo).
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("UN-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "unidades"
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"


class UnidadPorTipo(models.Model):
    """Relación muchos-a-muchos: qué unidades aplican a cada tipo de recurso."""
    tipo_recurso = models.ForeignKey(TipoRecurso, on_delete=models.CASCADE, related_name="unidades_permitidas")
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)

    class Meta:
        db_table = "unidades_por_tipo"
        unique_together = ("tipo_recurso", "unidad")


class Donacion(models.Model):
    ESTADO_CHOICES = [
        ("En acopio", "En acopio"),
        ("En tránsito", "En tránsito"),
        ("Recibida", "Recibida"),
        ("Entregado", "Entregado"),
        ("Distribuida", "Distribuida"),
        ("Cancelada", "Cancelada"),
    ]

    code = models.CharField(max_length=10, unique=True, editable=False)
    tipo = models.CharField(max_length=50)  # ej: "Alimentos no perecibles", "Ropa y abrigo", etc.
    cantidad = models.DecimalField(max_digits=12, decimal_places=2)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    tipo_recurso = models.ForeignKey(
        TipoRecurso, on_delete=models.PROTECT, null=True, blank=True
    )
    descripcion = models.TextField(blank=True, default="")
    origen = models.ForeignKey(
        Cuenta, on_delete=models.PROTECT, null=True, blank=True,
        related_name="donaciones_origen"
    )
    origen_display = models.CharField(max_length=200, blank=True, default="")
    centro = models.ForeignKey(
        Centro, on_delete=models.PROTECT, related_name="donaciones"
    )
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="En acopio")
    comprobante = models.CharField(max_length=100, blank=True, default="")
    # ── Microservicio de Pagos: para donaciones monetarias, el campo
    #    `comprobante` se pobla desde pagos-api. Ver clients/pago_client.py.
    # ── Microservicio de Logística: el tracking de envío se maneja
    #    via Envio (modelo separado abajo), que a futuro consultaría
    #    logistica-api.
    detalles = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("DO-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "donaciones"
        verbose_name = "Donación"
        verbose_name_plural = "Donaciones"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.code} - {self.tipo} - {self.estado}"


class Necesidad(models.Model):
    ESTADO_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("Asignado", "Asignado"),
        ("Cubierto", "Cubierto"),
        ("Cancelada", "Cancelada"),
    ]

    URGENCIA_CHOICES = [
        ("Alta", "Alta"),
        ("Media", "Media"),
        ("Baja", "Baja"),
    ]

    code = models.CharField(max_length=10, unique=True, editable=False)
    centro = models.ForeignKey(
        Centro, on_delete=models.PROTECT, related_name="necesidades"
    )
    tipo_recurso = models.ForeignKey(TipoRecurso, on_delete=models.PROTECT)
    cantidad_requerida = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_recibida = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT)
    urgencia = models.CharField(max_length=10, choices=URGENCIA_CHOICES, default="Media")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente")
    descripcion = models.TextField(blank=True, default="")
    fecha_limite = models.DateField(null=True, blank=True)
    reportado_por = models.CharField(max_length=200, blank=True, default="")
    creada_por = models.ForeignKey(
        Cuenta, on_delete=models.PROTECT, related_name="necesidades_creadas"
    )
    # ── Microservicio de Notificaciones: al activar/actualizar necesidad
    #    se notifica al creador via notif_client.py.
    detalles = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("NE-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "necesidades"
        verbose_name = "Necesidad"
        verbose_name_plural = "Necesidades"

    def __str__(self):
        return f"{self.code} - {self.centro.nombre} - {self.estado}"


class Propuesta(models.Model):
    ESTADO_CHOICES = [
        ("Pendiente", "Pendiente"),
        ("Aprobada", "Aprobada"),
        ("Rechazada", "Rechazada"),
    ]

    code = models.CharField(max_length=10, unique=True, editable=False)
    necesidad = models.ForeignKey(
        Necesidad, on_delete=models.CASCADE, related_name="propuestas"
    )
    usuario = models.ForeignKey(
        Cuenta, on_delete=models.PROTECT, related_name="propuestas"
    )
    mensaje = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("PR-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "propuestas"
        verbose_name = "Propuesta"
        verbose_name_plural = "Propuestas"

    def __str__(self):
        return f"{self.code} - {self.necesidad.code} - {self.estado}"


class Envio(models.Model):
    ESTADO_CHOICES = [
        ("Pendiente despacho", "Pendiente despacho"),
        ("En tránsito", "En tránsito"),
        ("Entregado", "Entregado"),
        ("Cancelado", "Cancelado"),
    ]

    code = models.CharField(max_length=10, unique=True, editable=False)
    donacion = models.ForeignKey(
        Donacion, on_delete=models.PROTECT, null=True, blank=True, related_name="envios"
    )
    centro = models.ForeignKey(
        Centro, on_delete=models.PROTECT, related_name="envios"
    )
    destino = models.CharField(max_length=300)
    fecha_salida = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendiente despacho")
    transportista = models.CharField(max_length=200, blank=True, default="")
    # ── Microservicio de Logística: a futuro estos datos se sincronizarían
    #    con logistica-api para tracking en tiempo real (GPS, rutas, etc.).
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("EN-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "envios"
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"

    def __str__(self):
        return f"{self.code} - {self.destino} - {self.estado}"


class Equipo(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    email = models.EmailField()
    foto_url = models.URLField(blank=True, default="")
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("EQ-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "equipo"
        verbose_name = "Miembro del Equipo"
        verbose_name_plural = "Miembros del Equipo"

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"


class Gobernanza(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    img_url = models.URLField(blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("GO-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "gobernanza"
        verbose_name = "Miembro de Gobernanza"
        verbose_name_plural = "Miembros de Gobernanza"

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"


class Hito(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    year = models.CharField(max_length=4)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, default="logro")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("HI-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "hitos"
        verbose_name = "Hito"
        verbose_name_plural = "Hitos"
        ordering = ["-year"]

    def __str__(self):
        return f"{self.titulo} ({self.year})"


class Valor(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("VA-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "valores"
        verbose_name = "Valor"
        verbose_name_plural = "Valores"

    def __str__(self):
        return self.titulo


class Reporte(models.Model):
    code = models.CharField(max_length=10, unique=True, editable=False)
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    tipo = models.CharField(max_length=10, default="PDF")  # PDF, XLSX
    size = models.CharField(max_length=10, blank=True, default="")
    archivo_url = models.URLField(blank=True, default="")
    icono = models.CharField(max_length=50, default="bi-file-earmark-pdf-fill")
    color = models.CharField(max_length=7, default="#DD4444")

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generar_code("RE-")
        super().save(*args, **kwargs)

    class Meta:
        db_table = "reportes"
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"

    def __str__(self):
        return self.titulo
