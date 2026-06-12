from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Donacion
from .serializers import DonacionSerializer

class DonacionViewSet(viewsets.ModelViewSet):
    queryset = Donacion.objects.all()
    serializer_class = DonacionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get("estado")
        centro_code = self.request.query_params.get("centro_code")
        tipo = self.request.query_params.get("tipo")
        if estado:
            qs = qs.filter(estado=estado)
        if centro_code:
            qs = qs.filter(centroId=centro_code)
        if tipo:
            qs = qs.filter(tipo=tipo)
        return qs

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        qs = self.get_queryset()
        total = qs.count()
        monetarias = qs.filter(tipo="Donación Monetaria")
        total_monto = monetarias.aggregate(s=Sum("cantidad"))["s"] or 0
        centros = qs.values("centroId").distinct().count()
        return Response({
            "total_donaciones": total,
            "total_monto": float(total_monto),
            "total_beneficiarios": 0,
            "centros_activos": centros,
            "por_estado": dict(qs.values_list("estado").annotate(c=Count("idDonacion"))),
            "por_tipo": dict(qs.values_list("tipo").annotate(c=Count("idDonacion"))),
        })