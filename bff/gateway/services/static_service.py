from ..clients import logistica_client
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

