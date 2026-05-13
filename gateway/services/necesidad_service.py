from ..schemas.necesidades import NecesidadOut, PropuestaOut
from ..exceptions import NotFoundError


async def list_all(estado=None, centro_code=None, urgencia=None) -> list[NecesidadOut]:
    return []


async def get_by_code(code: str) -> NecesidadOut:
    raise NotFoundError("Microservicio de necesidades no implementado")


async def create(body, rut: str) -> NecesidadOut:
    raise NotFoundError("Microservicio de necesidades no implementado")


async def update(code: str, body) -> NecesidadOut:
    raise NotFoundError("Microservicio de necesidades no implementado")


async def activar(code: str) -> NecesidadOut:
    raise NotFoundError("Microservicio de necesidades no implementado")


async def crear_propuesta(necesidad_code: str, mensaje: str, rut: str) -> PropuestaOut:
    raise NotFoundError("Microservicio de propuestas no implementado")


async def list_propuestas(necesidad_code: str) -> list[PropuestaOut]:
    return []
