from django.contrib import admin
from .models import CentroAcopio, Producto, Inventario

admin.site.register(CentroAcopio)
admin.site.register(Producto)
admin.site.register(Inventario)
