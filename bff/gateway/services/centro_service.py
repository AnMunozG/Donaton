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
        region=data.get("region", ""),
        direccion=data.get("direccion", ""),
        coordenadas=Coordenadas(lat=float(lat), lng=float(lng)) if lat is not None and lng is not None else None,
        encargado=data.get("encargado") or None,
        telefono=data.get("telefono", ""),
        capacidadTotal=data.get("capacidadTotal", 0),
        capacidadUsada=float(data.get("capacidadUsada", 0)),
        inventario=[],
        estado=data.get("estado", "Activo"),
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
        "region": body.region,
        "direccion": getattr(body, "direccion", ""),
        "telefono": getattr(body, "telefono", ""),
        "encargado": getattr(body, "encargado", ""),
        "capacidadTotal": body.capacidadTotal,
        "capacidadUsada": getattr(body, "capacidadUsada", 0),
        "estado": "Activo",
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
    if body.region is not None:
        payload["region"] = body.region
    if getattr(body, "direccion", None) is not None:
        payload["direccion"] = body.direccion
    if getattr(body, "telefono", None) is not None:
        payload["telefono"] = body.telefono
    if getattr(body, "encargado", None) is not None:
        payload["encargado"] = body.encargado
    if hasattr(body, "capacidadTotal") and body.capacidadTotal is not None:
        payload["capacidadTotal"] = body.capacidadTotal
    if hasattr(body, "capacidadUsada") and body.capacidadUsada is not None:
        payload["capacidadUsada"] = body.capacidadUsada
    if body.coordenadas is not None:
        payload["latitud"] = body.coordenadas.lat
        payload["longitud"] = body.coordenadas.lng
    if getattr(body, "estado", None) is not None:
        payload["estado"] = body.estado

    data = await logistica_client.actualizar_centro(id_, payload)
    if "error" in data or "detail" in data:
        raise ValidationError(data.get("error", data.get("detail", "Error al actualizar centro")))

    await publish_centro_actualizado(code, "actualizado")
    return _to_out(data)


async def get_inventario(code: str) -> list[InventarioItem]:
    try:
        id_ = int(code)
    except ValueError:
        raise NotFoundError("Centro no encontrado")

    items = await logistica_client.listar_inventario(params={"centro": id_})
    result = []
    for item in items if isinstance(items, list) else []:
        result.append(InventarioItem(
            tipo=item.get("productoNombre", str(item.get("producto", ""))),
            cantidad=str(item.get("cantidad", "0")),
        ))
    return result


async def get_stats(code: str) -> CentroStatsOut:
    try:
        centro = await get_by_code(code)
    except NotFoundError:
        raise
    return CentroStatsOut(
        id=centro.id, nombre=centro.nombre,
        total_donaciones=0, total_necesidades=0, capacidad_usada=centro.capacidadUsada,
    )
