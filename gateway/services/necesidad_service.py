from ..clients import donaciones_client, notif_client
from ..schemas.necesidades import NecesidadOut, PropuestaOut
from ..exceptions import NotFoundError, ValidationError
from ..events import publish_necesidad_creada, publish_necesidad_activada


def _to_out(data: dict) -> NecesidadOut:
    return NecesidadOut(
        id=data.get("code") or data.get("id", ""),
        recurso=data.get("recurso", ""),
        cantidad=float(data.get("cantidad", 0)),
        donado=float(data.get("donado", 0)),
        descripcion=data.get("descripcion", ""),
        unidad=data.get("unidad", ""),
        fecha=data.get("fecha", ""),
        urgencia=data.get("urgencia", "Media"),
        estado=data.get("estado", "Pendiente"),
        centroId=data.get("centroId", ""),
        centro=data.get("centro", ""),
        reportadoPor=data.get("reportadoPor", ""),
        detalles=data.get("detalles") or {},
    )


def _propuesta_out(data: dict) -> PropuestaOut:
    return PropuestaOut(
        code=data.get("code", ""),
        necesidad_code=data.get("necesidad_code", ""),
        usuario_rut=data.get("usuario_rut", ""),
        usuario_nombre=data.get("usuario_nombre", ""),
        mensaje=data.get("mensaje", ""),
        estado=data.get("estado", "Pendiente"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


async def list_all(estado=None, centro_code=None, urgencia=None) -> list[NecesidadOut]:
    params = {}
    if estado:
        params["estado"] = estado
    if centro_code:
        params["centro_code"] = centro_code
    if urgencia:
        params["urgencia"] = urgencia
    data = await donaciones_client.listar_necesidades(params=params or None)
    return [_to_out(n) for n in data]


async def get_by_code(code: str) -> NecesidadOut:
    data = await donaciones_client.obtener_necesidad(code)
    if not data or "error" in data:
        raise NotFoundError("Necesidad no encontrada")
    return _to_out(data)


async def create(body, rut: str) -> NecesidadOut:
    payload = {
        "centroId": body.centroId,
        "recurso": body.recurso,
        "cantidad": body.cantidad,
        "unidad": body.unidad,
        "descripcion": body.descripcion,
        "urgencia": body.urgencia,
        "reportadoPor": body.reportadoPor,
        "fecha_limite": body.fecha_limite,
        "detalles": body.detalles or {},
        "creado_por": rut,
    }
    data = await donaciones_client.crear_necesidad(payload)
    if "error" in data:
        raise ValidationError(data["error"])

    await publish_necesidad_creada(
        necesidad_code=data.get("code") or data.get("id", ""),
        centro_code=body.centroId,
        tipo_recurso=body.recurso,
        cantidad=body.cantidad,
    )
    return _to_out(data)


async def update(code: str, body) -> NecesidadOut:
    payload = {}
    if body.cantidad is not None:
        payload["cantidad"] = body.cantidad
    if body.urgencia is not None:
        payload["urgencia"] = body.urgencia
    if body.estado is not None:
        payload["estado"] = body.estado
    if body.descripcion is not None:
        payload["descripcion"] = body.descripcion
    if body.reportadoPor is not None:
        payload["reportadoPor"] = body.reportadoPor
    if body.detalles is not None:
        payload["detalles"] = body.detalles

    data = await donaciones_client.actualizar_necesidad(code, payload)
    if "error" in data:
        raise ValidationError(data["error"])
    return _to_out(data)


async def activar(code: str) -> NecesidadOut:
    data = await donaciones_client.activar_necesidad(code)
    if "error" in data:
        raise ValidationError(data["error"])

    await publish_necesidad_activada(code, data.get("centroId", ""))

    email = data.get("creador_email")
    if email:
        await notif_client.enviar_email(
            destino=email,
            asunto=f"Necesidad {code} activada",
            mensaje=f"Tu necesidad en {data.get('centro', '')} ha sido activada.",
        )
    return _to_out(data)


async def crear_propuesta(necesidad_code: str, mensaje: str, rut: str) -> PropuestaOut:
    payload = {
        "necesidad_code": necesidad_code,
        "mensaje": mensaje,
        "usuario_rut": rut,
    }
    data = await donaciones_client.crear_propuesta(payload)
    if "error" in data:
        raise ValidationError(data["error"])
    return _propuesta_out(data)


async def list_propuestas(necesidad_code: str) -> list[PropuestaOut]:
    data = await donaciones_client.listar_propuestas(necesidad_code)
    return [_propuesta_out(p) for p in data]
