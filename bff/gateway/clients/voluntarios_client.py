from .base import ServiceClient


class VoluntariosClient(ServiceClient):
    def __init__(self):
        super().__init__("VOLUNTARIOS_URL", "voluntarios")

    async def listar_voluntarios(self, params: dict = None) -> list:
        resp = await self.get("/api/voluntarios/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_voluntario(self, code: str) -> dict:
        return await self.get(f"/api/voluntarios/{code}/")

    async def crear_voluntario(self, data: dict) -> dict:
        return await self.post("/api/voluntarios/", data)

    async def actualizar_voluntario(self, code: str, data: dict) -> dict:
        return await self.patch(f"/api/voluntarios/{code}/", data)

    async def eliminar_voluntario(self, code: str) -> dict:
        return await self.delete(f"/api/voluntarios/{code}/")

    async def listar_horas(self, code: str) -> dict:
        return await self.get(f"/api/voluntarios/{code}/horas/")

    async def registrar_horas(self, code: str, data: dict) -> dict:
        return await self.post(f"/api/voluntarios/{code}/registrar-horas/", data)

    async def obtener_voluntario_por_rut(self, rut: str) -> dict | None:
        resultados = await self.listar_voluntarios(params={"rut": rut})
        if isinstance(resultados, list) and len(resultados) > 0:
            return resultados[0]
        return None
