from datetime import date
from asgiref.sync import sync_to_async
from django.db.models import Sum, Count, Q

from ..models import Donacion, Centro, Cuenta, Unidad
from ..schemas.donaciones import DonacionOut
from ..exceptions import NotFoundError, ValidationError
from ..clients.pago_client import cobrar


def _to_out(d: Donacion) -> DonacionOut:
    return DonacionOut(
        id=d.code, tipo=d.tipo,
        cantidad=str(int(float(d.cantidad))) if float(d.cantidad) == int(float(d.cantidad)) else str(float(d.cantidad)),
        unidad=d.unidad.nombre,
        origen=d.origen_display or (d.origen.nombre if d.origen else ""),
        centroId=d.centro.code, centro=d.centro.nombre,
        fecha=d.fecha.isoformat() if d.fecha else "",
        estado=d.estado, detalles=d.detalles or {},
        created_at=d.created_at, updated_at=d.updated_at,
    )


async def list_all(estado: str = None, centro_code: str = None, tipo: str = None) -> list[DonacionOut]:
    qs = Donacion.objects.select_related("centro", "origen", "unidad")
    if estado:
        qs = qs.filter(estado=estado)
    if centro_code:
        qs = qs.filter(centro__code=centro_code)
    if tipo:
        qs = qs.filter(tipo=tipo)
    return [_to_out(d) async for d in qs]


async def get_by_code(code: str) -> DonacionOut:
    try:
        return _to_out(await Donacion.objects.select_related("centro", "origen", "unidad").aget(code=code))
    except Donacion.DoesNotExist:
        raise NotFoundError("Donación no encontrada")


async def create(data, rut: str) -> DonacionOut:
    unidad = await Unidad.objects.filter(nombre__iexact=data.unidad).afirst()
    if not unidad:
        raise ValidationError(f"Unidad '{data.unidad}' no encontrada")
    try:
        centro = await Centro.objects.aget(code=data.centroId)
    except Centro.DoesNotExist:
        raise NotFoundError("Centro no encontrado")

    origen = None
    try:
        origen = await Cuenta.objects.aget(rut=data.origen)
    except Cuenta.DoesNotExist:
        pass

    donacion = Donacion(
        tipo=data.tipo, cantidad=data.cantidad, unidad=unidad,
        descripcion=data.detalles.get("descripcion", ""),
        origen=origen, origen_display=data.origen or (origen.nombre if origen else ""),
        centro=centro, fecha=date.fromisoformat(data.fecha) if data.fecha else date.today(),
        estado="En acopio", comprobante=data.comprobante, detalles=data.detalles or {},
    )
    await sync_to_async(donacion.save)()

    if data.tipo == "Donación Monetaria":
        await cobrar(monto=float(data.cantidad), origen=data.origen, descripcion=data.detalles.get("descripcion", ""))

    return _to_out(donacion)


async def update_estado(code: str, nuevo_estado: str) -> DonacionOut:
    try:
        d = await Donacion.objects.select_related("centro", "origen", "unidad").aget(code=code)
    except Donacion.DoesNotExist:
        raise NotFoundError("Donación no encontrada")
    if nuevo_estado not in [e[0] for e in Donacion.ESTADO_CHOICES]:
        raise ValidationError(f"Estado inválido. Válidos: {', '.join(e[0] for e in Donacion.ESTADO_CHOICES)}")
    d.estado = nuevo_estado
    await sync_to_async(d.save)()
    return _to_out(d)


async def get_stats() -> dict:
    stats = await Donacion.objects.aaggregate(total_monto=Sum("cantidad"))
    por_estado = {e: c async for e, c in Donacion.objects.values_list("estado").annotate(count=Count("id"))}
    por_tipo = {t["tipo"]: t["count"] async for t in Donacion.objects.values("tipo").annotate(count=Count("id"))}
    return {
        "total_donaciones": await Donacion.objects.acount(),
        "total_monto": float(stats["total_monto"] or 0),
        "total_beneficiarios": await Cuenta.objects.filter(~Q(rol="donante")).acount(),
        "centros_activos": await Centro.objects.filter(activo=True).acount(),
        "por_estado": por_estado,
        "por_tipo": por_tipo,
    }
