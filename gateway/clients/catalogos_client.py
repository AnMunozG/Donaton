from .base import ServiceClient


class CatalogosClient(ServiceClient):
    """Cliente para el microservicio de Catálogos (tipos de recurso, unidades, contenido estático)."""

    def __init__(self):
        super().__init__("CATALOGOS_URL", "catalogos")

    async def listar_tipos_recurso(self) -> list:
        resp = await self.get("/tipos-recurso")
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def listar_unidades(self) -> list:
        resp = await self.get("/unidades")
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def listar_equipo(self) -> list:
        resp = await self.get("/equipo")
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def listar_gobernanza(self) -> list:
        resp = await self.get("/gobernanza")
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def listar_hitos(self) -> list:
        resp = await self.get("/hitos")
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def listar_valores(self) -> list:
        resp = await self.get("/valores")
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def listar_reportes(self) -> list:
        resp = await self.get("/reportes")
        return resp if isinstance(resp, list) else resp.get("data", [])
