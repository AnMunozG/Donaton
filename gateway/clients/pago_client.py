from .base import ServiceClient


class PagoClient(ServiceClient):
    """Cliente para el microservicio de Pagos."""

    def __init__(self):
        super().__init__("PAGOS_URL", "pagos")

    async def cobrar(self, monto: float, origen: str, descripcion: str = "") -> dict:
        return await self.post("/cobrar", {"monto": monto, "origen": origen, "descripcion": descripcion})

    async def reembolsar(self, monto: float, origen: str) -> dict:
        return await self.post("/reembolso", {"monto": monto, "origen": origen})

    async def listar_transacciones(self, params: dict = None) -> dict:
        return await self.get("/transacciones", params=params)
