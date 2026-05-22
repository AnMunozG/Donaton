from .base import ServiceClient


class InventarioClient(ServiceClient):
    """Cliente para el microservicio de Inventario."""

    def __init__(self):
        super().__init__("INVENTARIO_URL", "inventario")

    async def listar_centros(self, params: dict = None) -> list:
        resp = await self.get("/centros", params=params)
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def obtener_centro(self, code: str) -> dict:
        return await self.get(f"/centros/{code}")

    async def crear_centro(self, data: dict) -> dict:
        return await self.post("/centros", data)

    async def actualizar_centro(self, code: str, data: dict) -> dict:
        return await self.put(f"/centros/{code}", data)

    async def obtener_stats_centro(self, code: str) -> dict:
        return await self.get(f"/centros/{code}/stats")
