from django.contrib import admin
from .models import Cuenta


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ("rut", "nombre", "email", "rol", "activo")
    list_filter = ("rol", "activo")
    search_fields = ("rut", "nombre", "email")
