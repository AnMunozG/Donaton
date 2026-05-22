from ..clients import logistica_client
from ..schemas.static import EnvioOut
from ..exceptions import NotFoundError


async def get_tipos_recurso():
    productos = await logistica_client.listar_productos()
    return [
        {"code": str(p["id"]), "nombre": p["nombre"], "descripcion": p.get("descripcion", ""), "activo": p.get("activo", True)}
        for p in productos
    ]


async def get_unidades():
    return []


async def get_equipo():
    return []


async def get_gobernanza():
    return []


async def get_hitos():
    return []


async def get_valores():
    return []


async def get_reportes():
    return []


async def get_envios() -> list[EnvioOut]:
    return []


async def get_envio(code: str) -> EnvioOut:
    raise NotFoundError("Microservicio de envíos no implementado")


async def create_envio(body) -> EnvioOut:
    raise NotFoundError("Microservicio de envíos no implementado")


async def update_envio(code: str, body) -> EnvioOut:
    raise NotFoundError("Microservicio de envíos no implementado")
