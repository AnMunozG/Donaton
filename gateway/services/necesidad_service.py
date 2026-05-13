from asgiref.sync import sync_to_async
from datetime import date

from ..models import Necesidad, Propuesta, Centro, Cuenta, TipoRecurso, Unidad
from ..schemas.necesidades import NecesidadOut, PropuestaOut
from ..exceptions import NotFoundError, ValidationError
from ..clients.notif_client import enviar_email


def _to_out(n: Necesidad) -> NecesidadOut:
    return NecesidadOut(
        id=n.code, recurso=n.tipo_recurso.nombre,
        cantidad=float(n.cantidad_requerida), donado=float(n.cantidad_recibida),
        descripcion=n.descripcion, unidad=n.unidad.nombre,
        fecha=n.created_at.isoformat() if n.created_at else "",
        urgencia=n.urgencia, estado=n.estado,
        centroId=n.centro.code, centro=n.centro.nombre,
        reportadoPor=n.reportado_por or (n.creada_por.nombre if n.creada_por else ""),
        detalles=n.detalles or {},
    )


async def list_all(estado=None, centro_code=None, urgencia=None) -> list[NecesidadOut]:
    qs = Necesidad.objects.select_related("centro", "tipo_recurso", "unidad", "creada_por")
    if estado:
        qs = qs.filter(estado=estado)
    if centro_code:
        qs = qs.filter(centro__code=centro_code)
    if urgencia:
        qs = qs.filter(urgencia=urgencia)
    return [_to_out(n) async for n in qs]


async def get_by_code(code: str) -> NecesidadOut:
    try:
        return _to_out(await Necesidad.objects.select_related("centro", "tipo_recurso", "unidad", "creada_por").aget(code=code))
    except Necesidad.DoesNotExist:
        raise NotFoundError("Necesidad no encontrada")


async def create(data, rut: str) -> NecesidadOut:
    try:
        centro = await Centro.objects.aget(code=data.centroId)
    except Centro.DoesNotExist:
        raise NotFoundError("Centro no encontrado")
    tipo_recurso = await TipoRecurso.objects.filter(nombre__iexact=data.recurso).afirst()
    if not tipo_recurso:
        raise NotFoundError(f"Tipo de recurso '{data.recurso}' no encontrado")
    unidad = await Unidad.objects.filter(nombre__iexact=data.unidad).afirst()
    if not unidad:
        raise NotFoundError(f"Unidad '{data.unidad}' no encontrada")
    try:
        creada_por = await Cuenta.objects.aget(rut=rut)
    except Cuenta.DoesNotExist:
        raise NotFoundError("Usuario no encontrado")

    necesidad = Necesidad(
        centro=centro, tipo_recurso=tipo_recurso, cantidad_requerida=data.cantidad,
        unidad=unidad, urgencia=data.urgencia, descripcion=data.descripcion,
        fecha_limite=date.fromisoformat(data.fecha_limite) if data.fecha_limite else None,
        reportado_por=data.reportadoPor, creada_por=creada_por,
        estado="Pendiente", detalles=data.detalles or {},
    )
    await sync_to_async(necesidad.save)()
    return _to_out(necesidad)


async def update(code: str, data) -> NecesidadOut:
    necesidad = await Necesidad.objects.select_related("centro", "tipo_recurso", "unidad", "creada_por").aget(code=code)
    for attr, field in [("cantidad", "cantidad_requerida"), ("urgencia", "urgencia"), ("estado", "estado"), ("descripcion", "descripcion"), ("reportadoPor", "reportado_por")]:
        val = getattr(data, attr, None)
        if val is not None:
            setattr(necesidad, field, val)
    if data.detalles is not None:
        necesidad.detalles = data.detalles
    await sync_to_async(necesidad.save)()
    return _to_out(necesidad)


async def activar(code: str) -> NecesidadOut:
    necesidad = await Necesidad.objects.select_related("centro", "tipo_recurso", "unidad", "creada_por").aget(code=code)
    if necesidad.estado != "Pendiente":
        raise ValidationError("Solo necesidades en estado Pendiente pueden activarse")
    necesidad.estado = "Asignado"
    await sync_to_async(necesidad.save)()
    if necesidad.creada_por and necesidad.creada_por.email:
        await enviar_email(destino=necesidad.creada_por.email, asunto=f"Necesidad {necesidad.code} activada", mensaje=f"Tu necesidad en {necesidad.centro.nombre} ha sido activada.")
    return _to_out(necesidad)


async def crear_propuesta(necesidad_code: str, mensaje: str, rut: str) -> Propuesta:
    try:
        necesidad = await Necesidad.objects.aget(code=necesidad_code)
    except Necesidad.DoesNotExist:
        raise NotFoundError("Necesidad no encontrada")
    try:
        usuario = await Cuenta.objects.aget(rut=rut)
    except Cuenta.DoesNotExist:
        raise NotFoundError("Usuario no encontrado")
    propuesta = Propuesta(necesidad=necesidad, usuario=usuario, mensaje=mensaje)
    await sync_to_async(propuesta.save)()
    return propuesta


async def list_propuestas(necesidad_code: str) -> list[Propuesta]:
    try:
        necesidad = await Necesidad.objects.aget(code=necesidad_code)
    except Necesidad.DoesNotExist:
        raise NotFoundError("Necesidad no encontrada")
    return [p async for p in Propuesta.objects.filter(necesidad=necesidad).select_related("usuario")]
