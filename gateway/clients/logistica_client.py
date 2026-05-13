from .base import ServiceClient


class LogisticaClient(ServiceClient):
    """Cliente para el microservicio de Logística."""

    def __init__(self):
        super().__init__("LOGISTICA_URL", "logistica")

    async def listar_envios(self, params: dict = None) -> list:
        resp = await self.get("/envios", params=params)
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def obtener_envio(self, code: str) -> dict:
        return await self.get(f"/envios/{code}")

    async def crear_envio(self, data: dict) -> dict:
        return await self.post("/envios", data)

    async def actualizar_envio(self, code: str, data: dict) -> dict:
        return await self.patch(f"/envios/{code}", data)
