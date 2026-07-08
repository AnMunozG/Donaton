from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Donacion, ItemDonacion
from .serializers import DonacionSerializer, ItemDonacionSerializer


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

    @action(detail=False, methods=["post"], url_path="multi")
    def crear_multi(self, request):
        data = request.data.copy()
        items_data = data.pop("items", [])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        donacion = serializer.save()

        items_creados = []
        for item_data in items_data:
            item = ItemDonacion.objects.create(donacion=donacion, **item_data)
            items_creados.append(item)

        out = DonacionSerializer(donacion).data
        out["items"] = ItemDonacionSerializer(items_creados, many=True).data
        return Response(out, status=status.HTTP_201_CREATED)

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
