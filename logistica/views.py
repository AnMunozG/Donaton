from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework import viewsets, permissions
from .models import Producto, CentroAcopio, Inventario
from .serializers import ProductoSerializer, CentroAcopioSerializer, InventarioSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAdminUser]

class CentroAcopioViewSet(viewsets.ModelViewSet):
    queryset = CentroAcopio.objects.all()
    serializer_class = CentroAcopioSerializer
    permission_classes = [permissions.IsAuthenticated]# Para que solo los usuarios autenticados puedan acceder a los centros de acopio, pero no necesariamente tengan que ser admin

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [permissions.IsAuthenticated]