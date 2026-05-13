from ..clients import catalogos_client, logistica_client, inventario_client
from ..schemas.static import EnvioOut
from ..exceptions import NotFoundError


def _envio_to_out(data: dict) -> EnvioOut:
    return EnvioOut(
        id=data.get("code") or data.get("id", ""),
        donacionId=data.get("donacionId"),
        centroId=data.get("centroId", ""),
        centro=data.get("centro", ""),
        destino=data.get("destino", ""),
        fechaSalida=data.get("fechaSalida"),
        fechaEntrega=data.get("fechaEntrega"),
        estado=data.get("estado", "Pendiente despacho"),
        transportista=data.get("transportista", ""),
    )


async def get_tipos_recurso():
    return await catalogos_client.listar_tipos_recurso()


async def get_unidades():
    return await catalogos_client.listar_unidades()


async def get_equipo():
    return await catalogos_client.listar_equipo()


async def get_gobernanza():
    return await catalogos_client.listar_gobernanza()


async def get_hitos():
    return await catalogos_client.listar_hitos()


async def get_valores():
    return await catalogos_client.listar_valores()


async def get_reportes():
    return await catalogos_client.listar_reportes()


async def get_envios() -> list[EnvioOut]:
    data = await logistica_client.listar_envios()
    return [_envio_to_out(e) for e in data]


async def get_envio(code: str) -> EnvioOut:
    data = await logistica_client.obtener_envio(code)
    if not data or "error" in data:
        raise NotFoundError("Envío no encontrado")
    return _envio_to_out(data)


async def create_envio(body) -> EnvioOut:
    payload = {
        "donacionId": body.donacionId,
        "centroId": body.centroId,
        "destino": body.destino,
        "fechaSalida": body.fechaSalida,
        "transportista": body.transportista,
    }
    data = await logistica_client.crear_envio(payload)
    return _envio_to_out(data)


async def update_envio(code: str, body) -> EnvioOut:
    payload = {}
    if body.estado is not None:
        payload["estado"] = body.estado
    if body.fechaSalida is not None:
        payload["fechaSalida"] = body.fechaSalida
    if body.fechaEntrega is not None:
        payload["fechaEntrega"] = body.fechaEntrega
    if body.transportista is not None:
        payload["transportista"] = body.transportista
    if body.destino is not None:
        payload["destino"] = body.destino
    data = await logistica_client.actualizar_envio(code, payload)
    return _envio_to_out(data)
