from django.contrib import admin
from .models import SeguimientoCentro, Agradecimiento

@admin.register(SeguimientoCentro)
class SeguimientoCentroAdmin(admin.ModelAdmin):
    list_display = ("usuario_rut", "centro_id", "fecha_inicio", "activo")
    list_filter = ("activo",)
    search_fields = ("usuario_rut", "centro_id")


@admin.register(Agradecimiento)
class AgradecimientoAdmin(admin.ModelAdmin):
    list_display = ("centro_id", "usuario_rut", "fecha", "resumen")
    search_fields = ("usuario_rut", "centro_id")
    list_filter = ("fecha",)

    def resumen(self, obj):
        return obj.mensaje[:60]
