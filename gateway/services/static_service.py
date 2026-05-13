from datetime import date
from ..models import TipoRecurso, Unidad, Equipo, Gobernanza, Hito, Valor, Reporte, Envio, Centro, Donacion
from ..exceptions import NotFoundError
from ..schemas.static import EnvioOut
from asgiref.sync import sync_to_async


def _envio_to_out(e: Envio) -> EnvioOut:
    return EnvioOut(
        id=e.code, donacionId=e.donacion.code if e.donacion else None,
        centroId=e.centro.code, centro=e.centro.nombre,
        destino=e.destino, transportista=e.transportista, estado=e.estado,
        fechaSalida=e.fecha_salida.isoformat() if e.fecha_salida else None,
        fechaEntrega=e.fecha_entrega.isoformat() if e.fecha_entrega else None,
    )


async def get_tipos_recurso(): return [t async for t in TipoRecurso.objects.filter(activo=True)]
async def get_unidades(): return [u async for u in Unidad.objects.all()]
async def get_equipo(): return [e async for e in Equipo.objects.filter(activo=True)]
async def get_gobernanza(): return [g async for g in Gobernanza.objects.all()]
async def get_hitos(): return [h async for h in Hito.objects.all()]
async def get_valores(): return [v async for v in Valor.objects.all()]
async def get_reportes(): return [r async for r in Reporte.objects.all()]

async def get_envios() -> list[EnvioOut]:
    return [_envio_to_out(e) async for e in Envio.objects.all().select_related("donacion", "centro")]

async def get_envio(code: str) -> EnvioOut:
    try:
        return _envio_to_out(await Envio.objects.select_related("donacion", "centro").aget(code=code))
    except Envio.DoesNotExist:
        raise NotFoundError("Envío no encontrado")

async def create_envio(data) -> EnvioOut:
    centro = await Centro.objects.aget(code=data.centroId)
    donacion = await Donacion.objects.aget(code=data.donacionId) if data.donacionId else None
    envio = Envio(donacion=donacion, centro=centro, destino=data.destino, transportista=data.transportista)
    await sync_to_async(envio.save)()
    return _envio_to_out(envio)

async def update_envio(code: str, data) -> EnvioOut:
    try:
        envio = await Envio.objects.select_related("donacion", "centro").aget(code=code)
    except Envio.DoesNotExist:
        raise NotFoundError("Envío no encontrado")
    if data.estado is not None:
        envio.estado = data.estado
    if data.fechaSalida is not None:
        envio.fecha_salida = date.fromisoformat(data.fechaSalida) if data.fechaSalida else None
    if data.fechaEntrega is not None:
        envio.fecha_entrega = date.fromisoformat(data.fechaEntrega) if data.fechaEntrega else None
    if data.transportista is not None:
        envio.transportista = data.transportista
    if data.destino is not None:
        envio.destino = data.destino
    await sync_to_async(envio.save)()
    return _envio_to_out(envio)
