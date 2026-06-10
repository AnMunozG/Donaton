from .base import ServiceClient

class DonacionesClient(ServiceClient):
    """Cliente para el microservicio de Donaciones (puerto 8002).
       Se conecta y consume los endpoints de forma directa y pública.
    """

    def __init__(self):
        super().__init__("DONACIONES_URL", "donaciones")

    # ── Donaciones ──

    async def listar_donaciones(self, params: dict = None) -> list:
        resp = await self.get("/api/donaciones/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_donacion(self, code: str) -> dict:
        return await self.get(f"/api/donaciones/{code}/")

    async def crear_donacion(self, data: dict) -> dict:
        return await self.post("/api/donaciones/", data)

    async def actualizar_estado_donacion(self, code: str, data: dict) -> dict:
        return await self.patch(f"/api/donaciones/{code}/", data)

    # ── Estadísticas ──

    async def obtener_estadisticas(self) -> dict:
        return await self.get("/api/donaciones/stats/")