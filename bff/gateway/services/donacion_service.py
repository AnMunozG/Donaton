from datetime import datetime
from ..schemas.donaciones import DonacionOut
from ..exceptions import NotFoundError
from . import centro_service

_donaciones = {}
_counter = 0


async def _centro_nombre(centro_id: str) -> str:
    try:
        c = await centro_service.get_by_code(centro_id)
        return c.nombre
    except Exception:
        return centro_id


async def list_all(estado: str = None, centro_code: str = None, tipo: str = None) -> list[DonacionOut]:
    items = list(_donaciones.values())
    if estado:
        items = [d for d in items if d["estado"] == estado]
    if centro_code:
        items = [d for d in items if d["centroId"] == centro_code]
    if tipo:
        items = [d for d in items if d["tipo"] == tipo]
    items.sort(key=lambda d: d.get("created_at", ""), reverse=True)
    return items


async def get_by_code(code: str) -> DonacionOut:
    d = _donaciones.get(code)
    if not d:
        raise NotFoundError("Donación no encontrada")
    return d


async def create(body, rut: str) -> DonacionOut:
    global _counter
    _counter += 1
    code = f"DON-{_counter:03d}"
    now = datetime.now()
    donacion = {
        "id": code,
        "tipo": body.tipo,
        "cantidad": str(body.cantidad),
        "unidad": body.unidad,
        "origen": body.origen or rut,
        "centroId": body.centroId,
        "centro": await _centro_nombre(body.centroId),
        "fecha": body.fecha or now.isoformat(),
        "estado": "En acopio",
        "detalles": body.detalles or {},
        "created_at": now,
        "updated_at": now,
    }
    _donaciones[code] = donacion
    return donacion


async def update_estado(code: str, nuevo_estado: str) -> DonacionOut:
    d = _donaciones.get(code)
    if not d:
        raise NotFoundError("Donación no encontrada")
    d["estado"] = nuevo_estado
    d["updated_at"] = datetime.now()
    return d


async def get_stats():
    total = len(_donaciones)
    centros = set(d["centroId"] for d in _donaciones.values())
    por_estado = {}
    por_tipo = {}
    for d in _donaciones.values():
        por_estado[d["estado"]] = por_estado.get(d["estado"], 0) + 1
        por_tipo[d["tipo"]] = por_tipo.get(d["tipo"], 0) + 1
    return {
        "total_donaciones": total,
        "total_monto": total * 10000,
        "total_beneficiarios": total * 3,
        "centros_activos": len(centros),
        "por_estado": por_estado,
        "por_tipo": por_tipo,
    }
