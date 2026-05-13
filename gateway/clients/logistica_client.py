from .base import ServiceClient


class LogisticaClient(ServiceClient):
    """Cliente para el microservicio de Logística (puerto 8001).

    Endpoints expuestos (vía DRF ModelViewSet):
      GET/POST     /api/productos/
      GET/PUT/DEL  /api/productos/{id}/
      GET/POST     /api/centros/
      GET/PUT/DEL  /api/centros/{id}/
      GET/POST     /api/inventario/
      GET/PUT/DEL  /api/inventario/{id}/
    """

    def __init__(self):
        super().__init__("LOGISTICA_URL", "logistica")

    # ── Productos ──

    async def listar_productos(self, params: dict = None) -> list:
        resp = await self.get("/api/productos/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_producto(self, id_: int) -> dict:
        return await self.get(f"/api/productos/{id_}/")

    # ── Centros ──

    async def listar_centros(self, params: dict = None) -> list:
        resp = await self.get("/api/centros/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_centro(self, id_: int) -> dict:
        return await self.get(f"/api/centros/{id_}/")

    async def crear_centro(self, data: dict) -> dict:
        return await self.post("/api/centros/", data)

    async def actualizar_centro(self, id_: int, data: dict) -> dict:
        return await self.put(f"/api/centros/{id_}/", data)

    async def eliminar_centro(self, id_: int) -> dict:
        return await self.delete(f"/api/centros/{id_}/")

    # ── Inventario ──

    async def listar_inventario(self, params: dict = None) -> list:
        resp = await self.get("/api/inventario/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_inventario(self, id_: int) -> dict:
        return await self.get(f"/api/inventario/{id_}/")
