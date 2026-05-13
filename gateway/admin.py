from django.contrib import admin
from .models import (
    Cuenta, Centro, TipoRecurso, Unidad, UnidadPorTipo,
    Donacion, Necesidad, Propuesta, Envio,
    Equipo, Gobernanza, Hito, Valor, Reporte,
)


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "email", "rol", "activo")
    list_filter = ("rol", "activo")
    search_fields = ("rut", "nombre", "email")


@admin.register(Centro)
class CentroAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "region", "capacidad", "estado", "activo")
    list_filter = ("region", "estado", "activo")
    search_fields = ("code", "nombre", "region")


@admin.register(TipoRecurso)
class TipoRecursoAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "activo")


@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ("code", "nombre", "abreviatura")


@admin.register(UnidadPorTipo)
class UnidadPorTipoAdmin(admin.ModelAdmin):
    list_display = ("tipo_recurso", "unidad")


@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ("code", "tipo", "cantidad", "estado", "centro", "fecha")
    list_filter = ("estado", "tipo")
    search_fields = ("code", "origen_display", "centro__nombre")


@admin.register(Necesidad)
class NecesidadAdmin(admin.ModelAdmin):
    list_display = ("code", "centro", "tipo_recurso", "urgencia", "estado")
    list_filter = ("estado", "urgencia")


@admin.register(Propuesta)
class PropuestaAdmin(admin.ModelAdmin):
    list_display = ("code", "necesidad", "usuario", "estado")
    list_filter = ("estado",)


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ("code", "destino", "estado", "transportista")
    list_filter = ("estado",)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cargo", "email", "activo")


@admin.register(Gobernanza)
class GobernanzaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cargo")


@admin.register(Hito)
class HitoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "year", "tipo")


@admin.register(Valor)
class ValorAdmin(admin.ModelAdmin):
    list_display = ("titulo", "icono")


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "tipo")
