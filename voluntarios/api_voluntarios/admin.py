from django.contrib import admin
from .models import Voluntario, RegistroHoras, AsignacionVoluntario


@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ["rut", "disponibilidad", "centro_preferido", "estado", "fecha_registro"]
    list_filter = ["estado", "disponibilidad"]
    search_fields = ["rut", "centro_preferido"]


@admin.register(RegistroHoras)
class RegistroHorasAdmin(admin.ModelAdmin):
    list_display = ["voluntario", "horas", "registrado_por_rut", "fecha"]
    list_filter = ["fecha"]
    search_fields = ["voluntario__rut", "registrado_por_rut"]


@admin.register(AsignacionVoluntario)
class AsignacionVoluntarioAdmin(admin.ModelAdmin):
    list_display = ["voluntario", "necesidad_id", "estado", "fecha_asignacion"]
    list_filter = ["estado"]
    search_fields = ["voluntario__rut"]
