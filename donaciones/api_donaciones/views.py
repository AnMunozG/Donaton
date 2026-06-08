from rest_framework import viewsets
from .models import Donacion
from .serializers import DonacionSerializer

class DonacionViewSet(viewsets.ModelViewSet):
    queryset = Donacion.objects.all()
    serializer_class = DonacionSerializer