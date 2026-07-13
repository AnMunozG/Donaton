from django.contrib import admin
from .models import Necesidad, EstadoNecesidad


@admin.register(Necesidad)
class NecesidadAdmin(admin.ModelAdmin):
    list_display = ["titulo", "categoria", "estado", "urgencia", "cantidad_requerida", "cantidad_recibida", "fecha_creacion"]
    list_filter = ["categoria", "estado", "urgencia"]
    search_fields = ["titulo", "solicitante_nombre"]


@admin.register(EstadoNecesidad)
class EstadoNecesidadAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
