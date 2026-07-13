from django.contrib import admin
from .models import Voluntario, VoluntarioCentro, RegistroHoras, AsignacionVoluntario, Notificacion


@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ["rut", "disponibilidad", "fecha_registro"]
    list_filter = ["disponibilidad"]
    search_fields = ["rut"]


@admin.register(VoluntarioCentro)
class VoluntarioCentroAdmin(admin.ModelAdmin):
    list_display = ["voluntario", "centro_id", "estado", "fecha_registro"]
    list_filter = ["estado", "centro_id"]
    search_fields = ["voluntario__rut", "centro_id"]


@admin.register(RegistroHoras)
class RegistroHorasAdmin(admin.ModelAdmin):
    list_display = ["voluntario", "centro_id", "horas", "registrado_por_rut", "fecha"]
    list_filter = ["fecha", "centro_id"]
    search_fields = ["voluntario__rut", "registrado_por_rut"]


@admin.register(AsignacionVoluntario)
class AsignacionVoluntarioAdmin(admin.ModelAdmin):
    list_display = ["voluntario", "necesidad_id", "estado", "fecha_asignacion"]
    list_filter = ["estado"]
    search_fields = ["voluntario__rut"]


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ["titulo", "voluntario", "leida", "enviado_por_rut", "fecha_creacion"]
    list_filter = ["leida", "fecha_creacion"]
    search_fields = ["voluntario__rut", "titulo"]
