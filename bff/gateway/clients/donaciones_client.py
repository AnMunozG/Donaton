from .base import ServiceClient


class DonacionesClient(ServiceClient):
    """Cliente para el microservicio de Donaciones."""

    def __init__(self):
        super().__init__("DONACIONES_URL", "donaciones")

    async def listar(self, params: dict = None) -> list:
        resp = await self.get("/donaciones", params=params)
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def obtener(self, code: str) -> dict:
        return await self.get(f"/donaciones/{code}")

    async def crear(self, data: dict) -> dict:
        return await self.post("/donaciones", data)

    async def actualizar_estado(self, code: str, estado: str) -> dict:
        return await self.patch(f"/donaciones/{code}/estado", {"estado": estado})

    async def obtener_stats(self) -> dict:
        return await self.get("/donaciones/stats")

    async def listar_necesidades(self, params: dict = None) -> list:
        resp = await self.get("/necesidades", params=params)
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def obtener_necesidad(self, code: str) -> dict:
        return await self.get(f"/necesidades/{code}")

    async def crear_necesidad(self, data: dict) -> dict:
        return await self.post("/necesidades", data)

    async def actualizar_necesidad(self, code: str, data: dict) -> dict:
        return await self.put(f"/necesidades/{code}", data)

    async def activar_necesidad(self, code: str) -> dict:
        return await self.post(f"/necesidades/{code}/activar")

    async def listar_propuestas(self, necesidad_code: str) -> list:
        resp = await self.get(f"/necesidades/{necesidad_code}/propuestas")
        return resp if isinstance(resp, list) else resp.get("data", [])

    async def crear_propuesta(self, data: dict) -> dict:
        return await self.post("/propuestas", data)
