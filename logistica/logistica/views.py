from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import CentroAcopio
from .permissions import IsAdminOrReadOnly
from .serializers import CentroAcopioSerializer

class CentroAcopioViewSet(viewsets.ModelViewSet):
    queryset = CentroAcopio.objects.all()
    serializer_class = CentroAcopioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
