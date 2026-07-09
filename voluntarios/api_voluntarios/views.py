from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from .models import Voluntario, RegistroHoras, AsignacionVoluntario
from .serializers import (
    VoluntarioSerializer, RegistroHorasSerializer, AsignacionVoluntarioSerializer,
)


class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get("estado")
        activo = self.request.query_params.get("activo")
        centro = self.request.query_params.get("centro_preferido")
        disponibilidad = self.request.query_params.get("disponibilidad")
        habilidad = self.request.query_params.get("habilidad")
        rut = self.request.query_params.get("rut")

        if estado:
            qs = qs.filter(estado=estado)
        elif activo is not None:
            if activo.lower() in ("true", "1", "yes"):
                qs = qs.filter(estado="activo")
            else:
                qs = qs.exclude(estado="activo")
        if centro:
            qs = qs.filter(centro_preferido=centro)
        if disponibilidad:
            qs = qs.filter(disponibilidad=disponibilidad)
        if habilidad:
            qs = qs.filter(habilidades__contains=habilidad)
        if rut:
            qs = qs.filter(rut=rut)

        return qs

    @action(detail=True, methods=["get"], url_path="horas")
    def listar_horas(self, request, pk=None):
        voluntario = self.get_object()
        registros = voluntario.registros_horas.all()
        serializer = RegistroHorasSerializer(registros, many=True)
        return Response({
            "horas_acumuladas": voluntario.horas_acumuladas,
            "registros": serializer.data,
        })

    @action(detail=True, methods=["post"], url_path="registrar-horas")
    def registrar_horas(self, request, pk=None):
        voluntario = self.get_object()
        horas = request.data.get("horas", 0)
        descripcion = request.data.get("descripcion", "")
        registrado_por = request.data.get("registrado_por_rut", "")

        try:
            horas = int(horas)
        except (ValueError, TypeError):
            return Response(
                {"error": "Las horas deben ser un número entero válido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if horas <= 0 or horas > 24:
            return Response(
                {"error": "Las horas deben estar entre 1 y 24"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not registrado_por:
            return Response(
                {"error": "El campo registrado_por_rut es obligatorio"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        registro = RegistroHoras.objects.create(
            voluntario=voluntario,
            horas=horas,
            descripcion=descripcion,
            registrado_por_rut=registrado_por,
        )

        serializer = RegistroHorasSerializer(registro)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AsignacionVoluntarioViewSet(viewsets.ModelViewSet):
    queryset = AsignacionVoluntario.objects.all()
    serializer_class = AsignacionVoluntarioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        voluntario_rut = self.request.query_params.get("rut")
        necesidad_id = self.request.query_params.get("necesidad_id")
        estado = self.request.query_params.get("estado")

        if voluntario_rut:
            qs = qs.filter(voluntario__rut=voluntario_rut)
        if necesidad_id:
            qs = qs.filter(necesidad_id=necesidad_id)
        if estado:
            qs = qs.filter(estado=estado)

        return qs
