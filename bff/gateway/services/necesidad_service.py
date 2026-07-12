from ..schemas.necesidades import NecesidadOut, PropuestaOut
from ..exceptions import NotFoundError, BffError
from ..clients.necesidades_client import NecesidadesClient
from . import centro_service

necesidades_client = NecesidadesClient()


async def _centro_nombre(centro_id: str) -> str:
    try:
        c = await centro_service.get_by_code(centro_id)
        return c.nombre
    except Exception:
        return centro_id


def _model_to_out(n: dict) -> dict:
    return {
        "id": str(n.get("id", "")),
        "recurso": n.get("titulo", ""),
        "cantidad": float(n.get("cantidad_requerida", 0)),
        "donado": float(n.get("cantidad_recibida", 0)),
        "descripcion": n.get("descripcion", ""),
        "unidad": n.get("unidad_medida", ""),
        "fecha": n.get("fecha_creacion", ""),
        "urgencia": n.get("urgencia", "").capitalize() if n.get("urgencia", "") else "",
        "estado": n.get("estado", "Pendiente"),
        "centroId": str(n.get("centro_acopio_id", "")),
        "centro": "",
        "reportadoPor": n.get("solicitante_nombre", ""),
        "detalles": n.get("detalles", {}),
    }


def _out_to_model(body) -> dict:
    try:
        centro_id_int = int(body.centroId)
    except (ValueError, TypeError):
        centro_id_int = body.centroId
    data = {
        "titulo": body.recurso,
        "descripcion": body.descripcion,
        "cantidad_requerida": int(float(body.cantidad)),
        "unidad_medida": body.unidad,
        "centro_acopio_id": centro_id_int,
        "solicitante_nombre": body.reportadoPor or "anónimo",
        "solicitante_contacto": "",
        "urgencia": (body.urgencia or "MEDIA").upper(),
        "estado": body.estado or "Activa",
        "detalles": body.detalles or {},
    }
    return data


async def _enrich(items: list) -> list:
    result = []
    for n in items:
        out = _model_to_out(n)
        out["centro"] = await _centro_nombre(out["centroId"])
        result.append(out)
    return result


async def _enrich_one(n: dict) -> dict:
    out = _model_to_out(n)
    out["centro"] = await _centro_nombre(out["centroId"])
    return out


async def list_all(estado=None, centro_code=None, urgencia=None, user=None) -> list[NecesidadOut]:
    try:
        params = {}
        if isinstance(user, dict) and user.get("rol") == "encargado":
            params["centro_id"] = user.get("centro_acopio_id")
        if estado:
            params["estado"] = estado
        if centro_code:
            params["centro_id"] = centro_code
        if urgencia:
            params["urgencia"] = urgencia
        items = await necesidades_client.listar_necesidades(params=params)
        enriched = await _enrich(items)
        enriched.sort(key=lambda n: n.get("fecha", ""), reverse=True)
        return enriched
    except Exception:
        return []


async def get_by_code(code: str) -> NecesidadOut:
    n = await necesidades_client.obtener_necesidad(code)
    if not n or "error" in n:
        raise NotFoundError("Necesidad no encontrada")
    return await _enrich_one(n)


async def create(body, rut: str) -> NecesidadOut:
    data = _out_to_model(body)
    if data.get("solicitante_nombre") == "anónimo" and rut != "anónimo":
        data["solicitante_nombre"] = rut
    n = await necesidades_client.crear_necesidad(data)
    if not n or "error" in n:
        raise Exception(n.get("error", "Error al crear necesidad") if isinstance(n, dict) else "Error al crear necesidad")
    return await _enrich_one(n)


async def update(code: str, body, user=None) -> NecesidadOut:
    n = await necesidades_client.obtener_necesidad(code)
    if not n or "error" in n:
        raise NotFoundError("Necesidad no encontrada")
    if isinstance(user, dict) and user.get("rol") == "encargado":
        if str(n.get("centro_acopio_id", "")) != str(user.get("centro_acopio_id", "")):
            raise BffError("No tienes permiso para modificar necesidades de otro centro", status=403)
    update_data = {}
    if body.cantidad is not None:
        update_data["cantidad_requerida"] = int(body.cantidad)
    if body.urgencia is not None:
        update_data["urgencia"] = body.urgencia.upper() if body.urgencia else ""
    if body.estado is not None:
        update_data["estado"] = body.estado
    if body.descripcion is not None:
        update_data["descripcion"] = body.descripcion
    if body.reportadoPor is not None:
        update_data["solicitante_nombre"] = body.reportadoPor
    if body.detalles is not None:
        update_data["detalles"] = body.detalles
    n = await necesidades_client.actualizar_necesidad(code, update_data)
    if not n or "error" in n:
        raise Exception(n.get("error", "Error al actualizar necesidad") if isinstance(n, dict) else "Error al actualizar necesidad")
    return await _enrich_one(n)


async def activar(code: str, urgencia: str = "MEDIA", user=None) -> NecesidadOut:
    n = await necesidades_client.obtener_necesidad(code)
    if not n or "error" in n:
        raise NotFoundError("Necesidad no encontrada")
    if isinstance(user, dict) and user.get("rol") == "encargado":
        if str(n.get("centro_acopio_id", "")) != str(user.get("centro_acopio_id", "")):
            raise BffError("No tienes permiso para activar necesidades de otro centro", status=403)
    update = {"estado": "Activa"}
    if urgencia:
        update["urgencia"] = urgencia.upper()
    n = await necesidades_client.actualizar_necesidad(code, update)
    if not n or "error" in n:
        raise Exception(n.get("error", "Error al activar necesidad") if isinstance(n, dict) else "Error al activar necesidad")
    return await _enrich_one(n)


async def crear_propuesta(necesidad_code: str, mensaje: str, rut: str) -> PropuestaOut:
    raise NotFoundError("Microservicio de propuestas no implementado")


async def list_propuestas(necesidad_code: str) -> list[PropuestaOut]:
    return []


async def list_ciudadanas() -> list[NecesidadOut]:
    try:
        items = await necesidades_client.listar_necesidades(params={"estado": "Pendiente"})
        enriched = await _enrich(items)
        enriched.sort(key=lambda n: n.get("fecha", ""), reverse=True)
        return enriched
    except Exception:
        return []


async def crear_ciudadana(body, rut: str) -> NecesidadOut:
    data = _out_to_model(body)
    data["estado"] = "Pendiente"
    data["urgencia"] = ""
    if data.get("solicitante_nombre") == "anónimo" and rut != "anónimo":
        data["solicitante_nombre"] = rut
    n = await necesidades_client.crear_necesidad(data)
    if "error" in n:
        raise Exception(n.get("error", "Error al crear necesidad ciudadana"))
    return await _enrich_one(n)


async def actualizar_ciudadana(code: str, body) -> NecesidadOut:
    n = await necesidades_client.obtener_necesidad(code)
    if not n or "error" in n:
        raise NotFoundError("Necesidad ciudadana no encontrada")
    update_data = {}
    if body.urgencia is not None:
        update_data["urgencia"] = body.urgencia.upper() if body.urgencia else ""
    if body.estado is not None:
        update_data["estado"] = body.estado
    if body.descripcion is not None:
        update_data["descripcion"] = body.descripcion
    if body.reportadoPor is not None:
        update_data["solicitante_nombre"] = body.reportadoPor
    n = await necesidades_client.actualizar_necesidad(code, update_data)
    if not n or "error" in n:
        raise Exception(n.get("error", "Error al actualizar necesidad ciudadana") if isinstance(n, dict) else "Error al actualizar necesidad ciudadana")
    return await _enrich_one(n)


async def eliminar_ciudadana(code: str) -> dict:
    n = await necesidades_client.obtener_necesidad(code)
    if not n or "error" in n:
        raise NotFoundError("Necesidad ciudadana no encontrada")
    await necesidades_client.eliminar_necesidad(code)
    return {"deleted": True}


async def delete(code: str) -> dict:
    n = await necesidades_client.obtener_necesidad(code)
    if not n or "error" in n:
        raise NotFoundError("Necesidad no encontrada")
    await necesidades_client.eliminar_necesidad(code)
    return {"deleted": True}
