from ..schemas.donaciones import DonacionOut
from ..exceptions import NotFoundError


async def list_all(estado: str = None, centro_code: str = None, tipo: str = None) -> list[DonacionOut]:
    return []


async def get_by_code(code: str) -> DonacionOut:
    raise NotFoundError("Microservicio de donaciones no implementado")


async def create(body, rut: str) -> DonacionOut:
    raise NotFoundError("Microservicio de donaciones no implementado")


async def update_estado(code: str, nuevo_estado: str) -> DonacionOut:
    raise NotFoundError("Microservicio de donaciones no implementado")


async def get_stats() -> dict:
    return {
        "total_donaciones": 0,
        "total_monto": 0,
        "total_beneficiarios": 0,
        "centros_activos": 0,
        "por_estado": {},
        "por_tipo": {},
    }
