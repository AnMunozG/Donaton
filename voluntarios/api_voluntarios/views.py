from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

from .models import Voluntario, VoluntarioCentro, RegistroHoras, AsignacionVoluntario, Notificacion
from .serializers import (
    VoluntarioSerializer, VoluntarioCentroSerializer,
    RegistroHorasSerializer, AsignacionVoluntarioSerializer,
    NotificacionSerializer,
)


class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        estado = self.request.query_params.get("estado")
        activo = self.request.query_params.get("activo")
        centro = self.request.query_params.get("centro_preferido") or self.request.query_params.get("centro_id")
        disponibilidad = self.request.query_params.get("disponibilidad")
        habilidad = self.request.query_params.get("habilidad")
        rut = self.request.query_params.get("rut")

        if rut:
            qs = qs.filter(rut=rut)
        if estado:
            qs = qs.filter(voluntario_centros__estado=estado).distinct()
        elif activo is not None:
            if activo.lower() in ("true", "1", "yes"):
                qs = qs.filter(voluntario_centros__estado="activo").distinct()
            else:
                qs = qs.exclude(voluntario_centros__estado="activo").distinct()
        if centro:
            qs = qs.filter(voluntario_centros__centro_id=centro).distinct()
        if disponibilidad:
            qs = qs.filter(disponibilidad=disponibilidad)
        if habilidad:
            qs = qs.filter(habilidades__contains=habilidad)

        return qs

    @action(detail=True, methods=["get"], url_path="horas")
    def listar_horas(self, request, pk=None):
        voluntario = self.get_object()
        centro_id = request.query_params.get("centro_id")
        registros = voluntario.registros_horas.all()
        if centro_id:
            registros = registros.filter(centro_id=centro_id)
        serializer = RegistroHorasSerializer(registros, many=True)
        horas_por_centro = {}
        for r in voluntario.registros_horas.all():
            cid = r.centro_id or ""
            horas_por_centro[cid] = horas_por_centro.get(cid, 0) + r.horas
        total = sum(horas_por_centro.values())
        return Response({
            "horas_acumuladas": total,
            "horas_por_centro": horas_por_centro,
            "registros": serializer.data,
        })

    @action(detail=True, methods=["post"], url_path="registrar-horas")
    def registrar_horas(self, request, pk=None):
        voluntario = self.get_object()
        horas = request.data.get("horas", 0)
        descripcion = request.data.get("descripcion", "")
        registrado_por = request.data.get("registrado_por_rut", "")
        centro_id = request.data.get("centro_id", "")

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

        if centro_id:
            assignment = VoluntarioCentro.objects.filter(
                voluntario=voluntario, centro_id=centro_id, estado="activo"
            ).first()
            if not assignment:
                return Response(
                    {"error": f"El voluntario no está activo en el centro {centro_id}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        registro = RegistroHoras.objects.create(
            voluntario=voluntario,
            centro_id=centro_id,
            horas=horas,
            descripcion=descripcion,
            registrado_por_rut=registrado_por,
        )

        serializer = RegistroHorasSerializer(registro)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VoluntarioCentroViewSet(viewsets.ModelViewSet):
    serializer_class = VoluntarioCentroSerializer

    def get_queryset(self):
        qs = VoluntarioCentro.objects.all()
        voluntario_id = self.request.query_params.get("voluntario_id")
        rut = self.request.query_params.get("rut")
        centro_id = self.request.query_params.get("centro_id")
        estado = self.request.query_params.get("estado")
        if voluntario_id:
            qs = qs.filter(voluntario_id=voluntario_id)
        if rut:
            qs = qs.filter(voluntario__rut=rut)
        if centro_id:
            qs = qs.filter(centro_id=centro_id)
        if estado:
            qs = qs.filter(estado=estado)
        return qs

    def create(self, request, *args, **kwargs):
        voluntario_id = request.data.get("voluntario")
        centro_id = request.data.get("centro_id", "")
        if not voluntario_id or not centro_id:
            return Response(
                {"error": "voluntario y centro_id son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        existing = VoluntarioCentro.objects.filter(
            voluntario_id=voluntario_id, centro_id=centro_id
        ).first()
        if existing:
            return Response(
                {"error": "Ya existe una solicitud para este centro",
                 "id": existing.id, "estado": existing.estado},
                status=status.HTTP_409_CONFLICT,
            )
        return super().create(request, *args, **kwargs)


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


class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        qs = Notificacion.objects.all()
        voluntario_id = self.request.query_params.get("voluntario_id")
        leida = self.request.query_params.get("leida")
        if voluntario_id:
            qs = qs.filter(voluntario_id=voluntario_id)
        if leida is not None:
            qs = qs.filter(leida=leida.lower() in ("true", "1", "yes"))
        return qs

    def create(self, request, *args, **kwargs):
        voluntario_id = request.data.get("voluntario_id") or request.data.get("voluntario")
        titulo = request.data.get("titulo", "")
        mensaje = request.data.get("mensaje", "")
        enviado_por = request.data.get("enviado_por_rut", "")
        if not voluntario_id or not titulo or not mensaje:
            return Response(
                {"error": "voluntario_id, titulo y mensaje son obligatorios"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        notif = Notificacion.objects.create(
            voluntario_id=voluntario_id,
            titulo=titulo,
            mensaje=mensaje,
            enviado_por_rut=enviado_por,
        )
        serializer = NotificacionSerializer(notif)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="marcar-leida")
    def marcar_leida(self, request, pk=None):
        notif = self.get_object()
        notif.leida = True
        notif.save()
        serializer = NotificacionSerializer(notif)
        return Response(serializer.data)
