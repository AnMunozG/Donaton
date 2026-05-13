from ..clients import inventario_client, catalogos_client
from ..schemas.centros import (
    CentroOut, CentroStatsOut, Coordenadas, InventarioItem,
)
from ..exceptions import NotFoundError, ValidationError
from ..events import publish_centro_actualizado


def _to_out(data: dict) -> CentroOut:
    coords = data.get("coordenadas")
    return CentroOut(
        id=data.get("code") or data.get("id", ""),
        nombre=data.get("nombre", ""),
        region=data.get("region", ""),
        direccion=data.get("direccion", ""),
        coordenadas=Coordenadas(lat=coords["lat"], lng=coords["lng"]) if coords and coords.get("lat") else None,
        encargado=data.get("encargado"),
        telefono=data.get("telefono", ""),
        capacidadTotal=data.get("capacidadTotal", 0),
        capacidadUsada=float(data.get("capacidadUsada", 0)),
        inventario=[InventarioItem(tipo=i["tipo"], cantidad=str(i["cantidad"])) for i in (data.get("inventario") or [])],
        estado=data.get("estado", "Activo"),
    )


async def list_all() -> list[CentroOut]:
    data = await inventario_client.listar_centros()
    return [_to_out(c) for c in data]


async def get_by_code(code: str) -> CentroOut:
    data = await inventario_client.obtener_centro(code)
    if not data or "error" in data:
        raise NotFoundError("Centro no encontrado")
    return _to_out(data)


async def create(body) -> CentroOut:
    payload = {
        "nombre": body.nombre,
        "region": body.region,
        "direccion": body.direccion,
        "telefono": body.telefono,
        "capacidadTotal": body.capacidadTotal,
    }
    if body.coordenadas:
        payload["coordenadas"] = {"lat": body.coordenadas.lat, "lng": body.coordenadas.lng}
    if getattr(body, "encargado_rut", None):
        payload["encargado_rut"] = body.encargado_rut
    data = await inventario_client.crear_centro(payload)
    if "error" in data:
        raise ValidationError(data["error"])
    return _to_out(data)


async def update(code: str, body) -> CentroOut:
    payload = {}
    for attr in ["nombre", "region", "direccion", "telefono", "estado"]:
        val = getattr(body, attr, None)
        if val is not None:
            payload[attr] = val
    if body.coordenadas is not None:
        payload["coordenadas"] = {"lat": body.coordenadas.lat, "lng": body.coordenadas.lng}
    if hasattr(body, "capacidadTotal") and body.capacidadTotal is not None:
        payload["capacidadTotal"] = body.capacidadTotal
    if body.inventario is not None:
        payload["inventario"] = [{"tipo": i.tipo, "cantidad": i.cantidad} for i in body.inventario]

    data = await inventario_client.actualizar_centro(code, payload)
    if "error" in data:
        raise ValidationError(data["error"])

    await publish_centro_actualizado(code, data.get("estado", ""))
    return _to_out(data)


async def get_stats(code: str) -> CentroStatsOut:
    try:
        data = await inventario_client.obtener_stats_centro(code)
    except Exception:
        centro = await get_by_code(code)
        return CentroStatsOut(
            id=centro.id, nombre=centro.nombre,
            total_donaciones=0, total_necesidades=0, capacidad_usada=0,
        )
    return CentroStatsOut(
        id=data.get("id") or code,
        nombre=data.get("nombre", ""),
        total_donaciones=data.get("total_donaciones", 0),
        total_necesidades=data.get("total_necesidades", 0),
        capacidad_usada=float(data.get("capacidad_usada", 0)),
    )
