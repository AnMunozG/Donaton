from ..clients import donaciones_client, pago_client
from ..schemas.donaciones import DonacionOut
from ..exceptions import NotFoundError, ValidationError
from ..events import publish_donacion_creada, publish_donacion_estado_cambiado


def _to_out(data: dict) -> DonacionOut:
    return DonacionOut(
        id=data.get("code") or data.get("id", ""),
        tipo=data.get("tipo", ""),
        cantidad=str(data.get("cantidad", "0")),
        unidad=data.get("unidad", ""),
        origen=data.get("origen", ""),
        centroId=data.get("centroId", "") or data.get("centro_code", ""),
        centro=data.get("centro", ""),
        fecha=data.get("fecha", ""),
        estado=data.get("estado", ""),
        detalles=data.get("detalles") or {},
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )


async def list_all(estado: str = None, centro_code: str = None, tipo: str = None) -> list[DonacionOut]:
    params = {}
    if estado:
        params["estado"] = estado
    if centro_code:
        params["centro_code"] = centro_code
    if tipo:
        params["tipo"] = tipo
    data = await donaciones_client.listar(params=params or None)
    return [_to_out(d) for d in data]


async def get_by_code(code: str) -> DonacionOut:
    data = await donaciones_client.obtener(code)
    if not data or "error" in data:
        raise NotFoundError("Donación no encontrada")
    return _to_out(data)


async def create(body, rut: str) -> DonacionOut:
    payload = {
        "tipo": body.tipo,
        "cantidad": body.cantidad,
        "unidad": body.unidad,
        "origen": body.origen or rut,
        "centroId": body.centroId,
        "fecha": body.fecha or "",
        "comprobante": body.comprobante,
        "detalles": body.detalles or {},
        "creado_por": rut,
    }
    data = await donaciones_client.crear(payload)
    if "error" in data:
        raise ValidationError(data["error"])

    await publish_donacion_creada(
        donacion_code=data.get("code") or data.get("id", ""),
        tipo=body.tipo,
        cantidad=body.cantidad,
        centro_code=body.centroId,
        origen=body.origen or rut,
    )

    if body.tipo == "Donación Monetaria":
        await pago_client.cobrar(monto=float(body.cantidad), origen=body.origen or rut)

    return _to_out(data)


async def update_estado(code: str, nuevo_estado: str) -> DonacionOut:
    data = await donaciones_client.actualizar_estado(code, nuevo_estado)
    if "error" in data:
        raise ValidationError(data["error"])

    await publish_donacion_estado_cambiado(code, "", nuevo_estado)
    return _to_out(data)


async def get_stats() -> dict:
    data = await donaciones_client.obtener_stats()
    return {
        "total_donaciones": data.get("total_donaciones", 0),
        "total_monto": float(data.get("total_monto", 0)),
        "total_beneficiarios": data.get("total_beneficiarios", 0),
        "centros_activos": data.get("centros_activos", 0),
        "por_estado": data.get("por_estado", {}),
        "por_tipo": data.get("por_tipo", {}),
    }
