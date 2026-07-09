from asgiref.sync import sync_to_async
from ..models import Agradecimiento
from ..schemas.agradecimientos import AgradecimientoCreate, AgradecimientoOut
from . import centro_service


@sync_to_async
def _list_agradecimientos(rut=None, centro_id=None):
    qs = Agradecimiento.objects.all()
    if rut:
        qs = qs.filter(usuario_rut=rut)
    if centro_id:
        qs = qs.filter(centro_id=centro_id)
    return list(qs.order_by("-fecha"))


@sync_to_async
def _create_agradecimiento(data):
    return Agradecimiento.objects.create(**data)


async def _enrich(agradecimientos):
    result = []
    for a in agradecimientos:
        centro_nombre = ""
        try:
            c = await centro_service.get_by_code(a.centro_id)
            centro_nombre = c.nombre
        except Exception:
            centro_nombre = a.centro_id
        result.append({
            "id": a.id,
            "centro_id": a.centro_id,
            "centro_nombre": centro_nombre,
            "usuario_rut": a.usuario_rut,
            "donacion_id": a.donacion_id,
            "mensaje": a.mensaje,
            "fecha": a.fecha,
        })
    return result


async def crear(data: AgradecimientoCreate) -> AgradecimientoOut:
    a = await _create_agradecimiento({
        "centro_id": data.centro_id,
        "usuario_rut": data.usuario_rut,
        "donacion_id": data.donacion_id,
        "mensaje": data.mensaje,
    })
    enriched = await _enrich([a])
    return AgradecimientoOut(**enriched[0])


async def listar_para_usuario(rut: str) -> list[AgradecimientoOut]:
    agradecimientos = await _list_agradecimientos(rut=rut)
    enriched = await _enrich(agradecimientos)
    return [AgradecimientoOut(**a) for a in enriched]


async def listar_para_centro(centro_id: str) -> list[AgradecimientoOut]:
    agradecimientos = await _list_agradecimientos(centro_id=centro_id)
    enriched = await _enrich(agradecimientos)
    return [AgradecimientoOut(**a) for a in enriched]
