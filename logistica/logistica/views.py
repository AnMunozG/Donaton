from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import Producto, CentroAcopio, Inventario
from .permissions import IsAdminOrReadOnly
from .serializers import ProductoSerializer, CentroAcopioSerializer, InventarioSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrReadOnly]#[IsAdminOrReadOnly][permissions.IsAdminUser]

class CentroAcopioViewSet(viewsets.ModelViewSet):
    queryset = CentroAcopio.objects.all()
    serializer_class = CentroAcopioSerializer
    permission_classes = [IsAdminOrReadOnly]#[IsAdminOrReadOnly][permissions.IsAuthenticated]

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer
    permission_classes = [IsAdminOrReadOnly]#[IsAdminOrReadOnly][permissions.IsAuthenticated]