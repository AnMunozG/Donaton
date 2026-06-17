from .base import ServiceClient

class NecesidadesClient(ServiceClient):
    def __init__(self):
        super().__init__("NECESIDADES_URL", "necesidades")

    async def listar_necesidades(self, params: dict = None) -> list:
        resp = await self.get("/api/necesidades/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_necesidad(self, code: str) -> dict:
        return await self.get(f"/api/necesidades/{code}/")

    async def crear_necesidad(self, data: dict) -> dict:
        return await self.post("/api/necesidades/", data)

    async def actualizar_necesidad(self, code: str, data: dict) -> dict:
        return await self.patch(f"/api/necesidades/{code}/", data)

    async def eliminar_necesidad(self, code: str) -> dict:
        return await self.delete(f"/api/necesidades/{code}/")
