from ..clients import logistica_client
from ..schemas.centros import CentroOut, CentroStatsOut, Coordenadas, InventarioItem
from ..exceptions import NotFoundError, ValidationError
from ..events import publish_centro_actualizado


def _to_out(data: dict) -> CentroOut:
    centro_id = data.get("idCentro") or data.get("id") or ""

    lat_raw = data.get("latitud")
    lng_raw = data.get("longitud")
    coordenadas_obj = None
    
    if lat_raw is not None and lng_raw is not None and lat_raw != "" and lng_raw != "":
        try:
            coordenadas_obj = Coordenadas(lat=float(lat_raw), lng=float(lng_raw))
        except (ValueError, TypeError):
            coordenadas_obj = None

    inventario_raw = data.get("inventario", []) or []
    inventario_mapeado = []
    
    if isinstance(inventario_raw, list):
        for item in inventario_raw:
            if isinstance(item, dict):
                inventario_mapeado.append(
                    InventarioItem(
                        tipo=str(item.get("item") or item.get("tipo") or ""),
                        cantidad=str(item.get("cantidad", "0"))
                    )
                )

    return CentroOut(
        id=str(centro_id),
        nombre=str(data.get("nombre", "")),
        region=str(data.get("region", "")),
        direccion=str(data.get("direccion", "")),
        coordenadas=coordenadas_obj,
        encargado=data.get("encargado") if data.get("encargado") else None,
        telefono=str(data.get("telefono", "")),
        capacidadTotal=int(data.get("capacidadTotal", 0)),
        capacidadUsada=float(data.get("capacidadUsada", 0.0)),
        inventario=inventario_mapeado,
        estado=str(data.get("estado", "Activo")),
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


def _calcular_estado(capacidad_total: int, capacidad_usada: int) -> str:
    if capacidad_total > 0 and (capacidad_usada / capacidad_total) >= 0.85:
        return "Capacidad crítica"
    return "Activo"


async def create(body) -> CentroOut:
    cap_total = body.capacidadTotal
    cap_usada = getattr(body, "capacidadUsada", 0)
    payload = {
        "nombre": body.nombre,
        "region": body.region,
        "direccion": getattr(body, "direccion", ""),
        "telefono": getattr(body, "telefono", ""),
        "encargado": getattr(body, "encargado", ""),
        "capacidadTotal": cap_total,
        "capacidadUsada": cap_usada,
        "inventario": [],
        "estado": _calcular_estado(cap_total, cap_usada),
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
    if hasattr(body, "inventario") and body.inventario is not None:
        payload["inventario"] = body.inventario
    if body.coordenadas is not None:
        payload["latitud"] = body.coordenadas.lat
        payload["longitud"] = body.coordenadas.lng
    if getattr(body, "estado", None) is not None:
        payload["estado"] = body.estado

    cap_total = payload.get("capacidadTotal")
    cap_usada = payload.get("capacidadUsada")
    if cap_total is not None or cap_usada is not None:
        if cap_total is None or cap_usada is None:
            current = await logistica_client.obtener_centro(id_)
            if current and "error" not in current:
                cap_total = cap_total if cap_total is not None else current.get("capacidadTotal", 0)
                cap_usada = cap_usada if cap_usada is not None else current.get("capacidadUsada", 0)
        payload["estado"] = _calcular_estado(cap_total or 0, cap_usada or 0)

    data = await logistica_client.actualizar_centro(id_, payload)
    if "error" in data or "detail" in data:
        raise ValidationError(data.get("error", data.get("detail", "Error al actualizar centro")))

    await publish_centro_actualizado(code, "actualizado")
    return _to_out(data)


async def get_inventario(code: str) -> list[InventarioItem]:
    """
    CORREGIDO: Ya no consulta la tabla intermedia obsoleta.
    Obtiene el centro y lee directamente el JSONField interno de inventario.
    """
    try:
        id_ = int(code)
    except ValueError:
        raise NotFoundError("Centro no encontrado")

    data = await logistica_client.obtener_centro(id_)
    if not data or "error" in data or "detail" in data:
        raise NotFoundError("Centro no encontrado")

    inventario_raw = data.get("inventario", []) or []
    
    return [
        InventarioItem(
            tipo=item.get("item", ""),
            cantidad=str(item.get("cantidad", "0"))
        ) for item in inventario_raw
    ]


async def delete(code: str) -> None:
    try:
        id_ = int(code)
    except ValueError:
        raise NotFoundError("Centro no encontrado")
    await logistica_client.eliminar_centro(id_)


async def get_stats(code: str) -> CentroStatsOut:
    try:
        centro = await get_by_code(code)
    except NotFoundError:
        raise
    return CentroStatsOut(
        id=centro.id, nombre=centro.nombre,
        total_donaciones=0, total_necesidades=0, capacidad_usada=centro.capacidadUsada,
    )