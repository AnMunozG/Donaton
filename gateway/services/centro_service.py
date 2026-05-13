from ..clients import logistica_client
from ..schemas.centros import CentroOut, CentroStatsOut, Coordenadas, InventarioItem
from ..exceptions import NotFoundError, ValidationError
from ..events import publish_centro_actualizado


def _to_out(data: dict) -> CentroOut:
    lat = data.get("latitud")
    lng = data.get("longitud")
    return CentroOut(
        id=str(data.get("id", "")),
        nombre=data.get("nombre", ""),
        region="",
        direccion=data.get("direccion", ""),
        coordenadas=Coordenadas(lat=float(lat), lng=float(lng)) if lat is not None and lng is not None else None,
        encargado=None,
        telefono="",
        capacidadTotal=data.get("capacidadTotal", 0),
        capacidadUsada=float(data.get("capacidadUsada", 0)),
        inventario=[],
        estado="Activo",
    )


async def list_all() -> list[CentroOut]:
    data = await logistica_client.listar_centros()
    return [_to_out(c) for c in data]


async def get_by_code(code: str) -> CentroOut:
    try:
        id_ = int(code)
    except ValueError:
        raise NotFoundError("Centro no encontrado")
    data = await logistica_client.obtener_centro(id_)
    if not data or "error" in data or "detail" in data:
        raise NotFoundError("Centro no encontrado")
    return _to_out(data)


async def create(body) -> CentroOut:
    payload = {
        "nombre": body.nombre,
        "direccion": body.direccion,
        "capacidadTotal": body.capacidadTotal,
    }
    if body.coordenadas:
        payload["latitud"] = body.coordenadas.lat
        payload["longitud"] = body.coordenadas.lng
    data = await logistica_client.crear_centro(payload)
    if "error" in data or "detail" in data:
        raise ValidationError(data.get("error", data.get("detail", "Error al crear centro")))
    return _to_out(data)


async def update(code: str, body) -> CentroOut:
    try:
        id_ = int(code)
    except ValueError:
        raise NotFoundError("Centro no encontrado")

    payload = {}
    if body.nombre is not None:
        payload["nombre"] = body.nombre
    if body.direccion is not None:
        payload["direccion"] = body.direccion
    if hasattr(body, "capacidadTotal") and body.capacidadTotal is not None:
        payload["capacidadTotal"] = body.capacidadTotal
    if body.coordenadas is not None:
        payload["latitud"] = body.coordenadas.lat
        payload["longitud"] = body.coordenadas.lng

    if getattr(body, "inventario", None) is not None:
        pass
    if getattr(body, "estado", None) is not None:
        pass

    data = await logistica_client.actualizar_centro(id_, payload)
    if "error" in data or "detail" in data:
        raise ValidationError(data.get("error", data.get("detail", "Error al actualizar centro")))

    await publish_centro_actualizado(code, "actualizado")
    return _to_out(data)


async def get_stats(code: str) -> CentroStatsOut:
    try:
        centro = await get_by_code(code)
    except NotFoundError:
        raise
    return CentroStatsOut(
        id=centro.id, nombre=centro.nombre,
        total_donaciones=0, total_necesidades=0, capacidad_usada=centro.capacidadUsada,
    )
