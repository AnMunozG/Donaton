from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Count, Sum
from .models import Donacion
from .serializers import DonacionSerializer, ItemDonacionSerializer


class DonacionViewSet(viewsets.ModelViewSet):
    queryset = Donacion.objects.select_related("estado").all()
    serializer_class = DonacionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get("estado")
        centro_code = self.request.query_params.get("centro_code")
        tipo = self.request.query_params.get("tipo")
        origen = self.request.query_params.get("origen")
        if estado:
            qs = qs.filter(estado__nombre=estado)
        if centro_code:
            qs = qs.filter(centroId=centro_code)
        if tipo:
            qs = qs.filter(tipo=tipo)
        if origen:
            qs = qs.filter(origen=origen)
        return qs

    @action(detail=False, methods=["post"], url_path="multi")
    def crear_multi(self, request):
        data = request.data.copy()
        items_data = data.pop("items", [])

        if not isinstance(items_data, list) or len(items_data) == 0:
            return Response(
                {"items": "Debes enviar al menos un artículo (items) para la donación."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validamos TODOS los items antes de tocar la base de datos, para no
        # dejar una Donacion "huérfana" (sin items) si alguno viene mal.
        item_serializers = []
        errores_items = {}
        for idx, item_data in enumerate(items_data):
            if not isinstance(item_data, dict):
                errores_items[idx] = "El artículo debe ser un objeto con tipo, cantidad, unidad y detalles."
                continue
            item_serializer = ItemDonacionSerializer(data=item_data)
            if not item_serializer.is_valid():
                errores_items[idx] = item_serializer.errors
            else:
                item_serializers.append(item_serializer)

        if errores_items:
            return Response({"items": errores_items}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            donacion = serializer.save()
            items_creados = [
                item_serializer.save(donacion=donacion) for item_serializer in item_serializers
            ]

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
            "por_estado": dict(qs.values_list("estado__nombre").annotate(c=Count("idDonacion"))),
            "por_tipo": dict(qs.values_list("tipo").annotate(c=Count("idDonacion"))),
        })
        