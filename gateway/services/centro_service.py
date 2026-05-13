from asgiref.sync import sync_to_async

from ..models import Centro, Cuenta, Donacion, Necesidad
from ..schemas.centros import CentroOut, CentroStatsOut, Coordenadas, InventarioItem
from ..exceptions import NotFoundError, ValidationError


def _to_out(c: Centro) -> CentroOut:
    return CentroOut(
        id=c.code,
        nombre=c.nombre,
        region=c.region,
        direccion=c.direccion,
        coordenadas=Coordenadas(lat=float(c.coordenadas_lat), lng=float(c.coordenadas_lng)) if c.coordenadas_lat is not None else None,
        encargado=c.encargado.nombre if c.encargado else None,
        telefono=c.telefono,
        capacidadTotal=c.capacidad,
        capacidadUsada=0.0,
        inventario=[InventarioItem(tipo=i["tipo"], cantidad=i["cantidad"]) for i in (c.inventario or [])],
        estado=c.estado,
    )


async def list_all() -> list[CentroOut]:
    return [_to_out(c) async for c in Centro.objects.filter(activo=True).select_related("encargado")]


async def get_by_code(code: str) -> CentroOut:
    try:
        return _to_out(await Centro.objects.select_related("encargado").aget(code=code))
    except Centro.DoesNotExist:
        raise NotFoundError("Centro no encontrado")


async def create(data) -> CentroOut:
    centro = Centro(
        nombre=data.nombre, region=data.region, direccion=data.direccion,
        telefono=getattr(data, "telefono", ""),
        capacidad=data.capacidadTotal if hasattr(data, "capacidadTotal") else getattr(data, "capacidad", 0),
    )
    if data.coordenadas:
        centro.coordenadas_lat = data.coordenadas.lat
        centro.coordenadas_lng = data.coordenadas.lng
    if getattr(data, "encargado_rut", None):
        try:
            centro.encargado = await Cuenta.objects.aget(rut=data.encargado_rut)
        except Cuenta.DoesNotExist:
            raise ValidationError("Encargado no encontrado")
    await sync_to_async(centro.save)()
    return _to_out(centro)


async def update(code: str, data) -> CentroOut:
    try:
        centro = await Centro.objects.select_related("encargado").aget(code=code)
    except Centro.DoesNotExist:
        raise NotFoundError("Centro no encontrado")
    for attr in ["nombre", "region", "direccion", "telefono", "estado"]:
        val = getattr(data, attr, None)
        if val is not None:
            setattr(centro, attr, val)
    if data.coordenadas is not None:
        centro.coordenadas_lat = data.coordenadas.lat
        centro.coordenadas_lng = data.coordenadas.lng
    if hasattr(data, "capacidadTotal") and data.capacidadTotal is not None:
        centro.capacidad = data.capacidadTotal
    if data.inventario is not None:
        centro.inventario = [{"tipo": i.tipo, "cantidad": i.cantidad} for i in data.inventario]
    await sync_to_async(centro.save)()
    return _to_out(centro)


async def get_stats(code: str) -> CentroStatsOut:
    try:
        centro = await Centro.objects.aget(code=code)
    except Centro.DoesNotExist:
        raise NotFoundError("Centro no encontrado")
    return {
        "id": centro.code,
        "nombre": centro.nombre,
        "total_donaciones": await Donacion.objects.filter(centro=centro).acount(),
        "total_necesidades": await Necesidad.objects.filter(centro=centro).acount(),
        "capacidad_usada": centro.capacidad_usada,
    }
