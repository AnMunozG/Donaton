from datetime import datetime
from ..schemas.necesidades import NecesidadOut, PropuestaOut
from ..exceptions import NotFoundError
from . import centro_service

_necesidades = {}
_ciudadanas = {}
_counter = 0
_ciudadana_counter = 0


async def _centro_nombre(centro_id: str) -> str:
    try:
        c = await centro_service.get_by_code(centro_id)
        return c.nombre
    except Exception:
        return centro_id


async def list_all(estado=None, centro_code=None, urgencia=None) -> list[NecesidadOut]:
    items = list(_necesidades.values())
    if estado:
        items = [n for n in items if n["estado"] == estado]
    if centro_code:
        items = [n for n in items if n["centroId"] == centro_code]
    if urgencia:
        items = [n for n in items if n["urgencia"] == urgencia]
    items.sort(key=lambda n: n.get("created_at", ""), reverse=True)
    return items


async def get_by_code(code: str) -> NecesidadOut:
    n = _necesidades.get(code)
    if not n:
        raise NotFoundError("Necesidad no encontrada")
    return n


async def create(body, rut: str) -> NecesidadOut:
    global _counter
    _counter += 1
    code = f"NEC-{_counter:03d}"
    now = datetime.now()
    necesidad = {
        "id": code,
        "recurso": body.recurso,
        "cantidad": body.cantidad,
        "donado": 0,
        "descripcion": body.descripcion or "",
        "unidad": body.unidad,
        "fecha": now.isoformat(),
        "urgencia": body.urgencia or "Media",
        "estado": body.estado or "Activa",
        "centroId": body.centroId,
        "centro": await _centro_nombre(body.centroId),
        "reportadoPor": body.reportadoPor or rut,
        "detalles": body.detalles or {},
    }
    _necesidades[code] = necesidad
    return necesidad


async def update(code: str, body) -> NecesidadOut:
    n = _necesidades.get(code)
    if not n:
        raise NotFoundError("Necesidad no encontrada")
    if body.cantidad is not None:
        n["cantidad"] = body.cantidad
    if body.urgencia is not None:
        n["urgencia"] = body.urgencia
    if body.estado is not None:
        n["estado"] = body.estado
    if body.descripcion is not None:
        n["descripcion"] = body.descripcion
    if body.reportadoPor is not None:
        n["reportadoPor"] = body.reportadoPor
    if body.detalles is not None:
        n["detalles"] = body.detalles
    return n


async def activar(code: str) -> NecesidadOut:
    n = _ciudadanas.get(code)
    if not n:
        raise NotFoundError("Necesidad ciudadana no encontrada")
    global _counter
    _counter += 1
    new_code = f"NEC-{_counter:03d}"
    necesidad = {**n, "id": new_code, "estado": "Activa"}
    _necesidades[new_code] = necesidad
    del _ciudadanas[code]
    return necesidad


async def crear_propuesta(necesidad_code: str, mensaje: str, rut: str) -> PropuestaOut:
    raise NotFoundError("Microservicio de propuestas no implementado")


async def list_propuestas(necesidad_code: str) -> list[PropuestaOut]:
    return []


# ── Necesidades ciudadanas (inbox para admin) ──

async def list_ciudadanas() -> list[NecesidadOut]:
    items = list(_ciudadanas.values())
    items.sort(key=lambda n: n.get("created_at", ""), reverse=True)
    return items


async def crear_ciudadana(body, rut: str) -> NecesidadOut:
    global _ciudadana_counter
    _ciudadana_counter += 1
    code = f"CIU-{_ciudadana_counter:03d}"
    now = datetime.now()
    necesidad = {
        "id": code,
        "recurso": body.recurso,
        "cantidad": body.cantidad,
        "donado": 0,
        "descripcion": body.descripcion or "",
        "unidad": body.unidad,
        "fecha": now.isoformat(),
        "urgencia": body.urgencia or "",
        "estado": "Pendiente",
        "centroId": body.centroId,
        "centro": await _centro_nombre(body.centroId),
        "reportadoPor": body.reportadoPor or rut,
        "detalles": body.detalles or {},
    }
    _ciudadanas[code] = necesidad
    return necesidad


async def actualizar_ciudadana(code: str, body) -> NecesidadOut:
    n = _ciudadanas.get(code)
    if not n:
        raise NotFoundError("Necesidad ciudadana no encontrada")
    if body.urgencia is not None:
        n["urgencia"] = body.urgencia
    if body.estado is not None:
        n["estado"] = body.estado
    if body.descripcion is not None:
        n["descripcion"] = body.descripcion
    if body.reportadoPor is not None:
        n["reportadoPor"] = body.reportadoPor
    return n


async def eliminar_ciudadana(code: str) -> dict:
    if code not in _ciudadanas:
        raise NotFoundError("Necesidad ciudadana no encontrada")
    del _ciudadanas[code]
    return {"deleted": True}
