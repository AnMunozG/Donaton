from asgiref.sync import sync_to_async
from ..models import SeguimientoCentro
from ..schemas.seguimiento import SeguimientoOut
from . import centro_service


@sync_to_async
def _get_or_create_seguimiento(rut, centro_id):
    obj, created = SeguimientoCentro.objects.get_or_create(
        usuario_rut=rut, centro_id=centro_id,
        defaults={"activo": True},
    )
    if not created and not obj.activo:
        obj.activo = True
        obj.save()
    return obj


@sync_to_async
def _deactivate_seguimiento(rut, centro_id):
    try:
        obj = SeguimientoCentro.objects.get(usuario_rut=rut, centro_id=centro_id)
        obj.activo = False
        obj.save()
    except SeguimientoCentro.DoesNotExist:
        pass


@sync_to_async
def _list_seguimientos(rut):
    return list(
        SeguimientoCentro.objects.filter(usuario_rut=rut, activo=True).order_by("-fecha_inicio")
    )


@sync_to_async
def _check_seguido(rut, centro_id):
    return SeguimientoCentro.objects.filter(
        usuario_rut=rut, centro_id=centro_id, activo=True
    ).exists()


async def listar_centros_dict():
    try:
        centros = await centro_service.list_all()
        return {c.id: c.nombre for c in centros}
    except Exception:
        return {}


async def seguir(rut: str, centro_id: str) -> SeguimientoOut:
    obj = await _get_or_create_seguimiento(rut, centro_id)
    centros_dict = await listar_centros_dict()
    return SeguimientoOut(
        centro_id=obj.centro_id,
        centro_nombre=centros_dict.get(obj.centro_id, obj.centro_id),
        fecha_inicio=obj.fecha_inicio,
        activo=obj.activo,
    )


async def dejar_de_seguir(rut: str, centro_id: str) -> None:
    await _deactivate_seguimiento(rut, centro_id)


async def listar_seguidos(rut: str) -> list[SeguimientoOut]:
    seguimientos = await _list_seguimientos(rut)
    centros_dict = await listar_centros_dict()
    return [
        SeguimientoOut(
            centro_id=s.centro_id,
            centro_nombre=centros_dict.get(s.centro_id, s.centro_id),
            fecha_inicio=s.fecha_inicio,
            activo=s.activo,
        )
        for s in seguimientos
    ]


async def es_seguido(rut: str, centro_id: str) -> bool:
    return await _check_seguido(rut, centro_id)
