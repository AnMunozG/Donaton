from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'rut', 'email', 'first_name', 'is_staff')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Chilena', {'fields': ('rut',)}),
    )
    
    # Agregar el campo 'rut' al formulario de creación de usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Chilena', {'fields': ('rut',)}),
    )