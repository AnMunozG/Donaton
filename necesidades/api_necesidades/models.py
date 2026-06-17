from django.db import models

class Necesidad(models.Model):
    CATEGORIAS = [
        ('ALIMENTOS', 'Alimentos y Víveres'),
        ('ROPA', 'Ropa y Abrigo'),
        ('DINERO', 'Aporte Económico'),
        ('SALUD', 'Insumos Médicos'),
        ('UTILES', 'Útiles de Aseo / Limpieza'),
        ('VOLUNTARIADO', 'Voluntariado / Mano de Obra'),
        ('OTROS', 'Otros'),
    ]
    
    ESTADOS = [
        ('PENDIENTE', 'Pendiente de Validación'),
        ('APROBADA', 'Activa / Buscando Donaciones'),
        ('EN_PROCESO', 'En Camino / Asignada'),
        ('CUBIERTA', 'Meta Alcanzada / Finalizada'),
        ('RECHAZADA', 'Rechazada / Cancelada'),
    ]

    # --- Relación Inter-Microservicios (Logística) ---
    # Guardamos solo el ID del centro de acopio. Logística nos dirá el nombre y dirección mediante este ID.
    centro_acopio_id = models.PositiveIntegerField(
        verbose_name="ID del Centro de Acopio destino",
        help_text="Enlace lógico al microservicio de Logística"
    )

    # --- Información de la Necesidad ---
    titulo = models.CharField(max_length=150, verbose_name="Título corto (ej: Pañales para niños)")
    descripcion = models.TextField(verbose_name="Detalle de la urgencia o requerimiento")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='OTROS')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    
    # --- Control de Cantidades y Trazabilidad ---
    cantidad_requerida = models.PositiveIntegerField(default=1, verbose_name="Cantidad Total Necesitada")
    cantidad_recibida = models.PositiveIntegerField(default=0, verbose_name="Cantidad Recibida Actual")
    unidad_medida = models.CharField(max_length=30, default="unidades", help_text="ej: kg, litros, cajas, unidades")

    # --- Datos de Contacto/Validación ---
    solicitante_nombre = models.CharField(max_length=100, verbose_name="Nombre de quien solicita / Organización")
    solicitante_contacto = models.CharField(max_length=150, verbose_name="Contacto (Teléfono o Email)")
    
    # --- Auditoría ---
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Necesidad"
        verbose_name_plural = "Necesidades"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"[{self.estado}] {self.titulo} para Centro #{self.centro_acopio_id}"

    @property
    def porcentaje_cubierto(self):
        """Calcula automáticamente el avance de la recaudación para el Frontend"""
        if self.cantidad_requerida == 0:
            return 100
        porcentaje = (self.cantidad_recibida / self.cantidad_requerida) * 100
        return min(round(porcentaje, 2), 100.0)