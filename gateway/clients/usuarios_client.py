from .base import ServiceClient


class UsuariosClient(ServiceClient):
    """Cliente para el microservicio de Usuarios (puerto 8000).

    Algunos endpoints requieren JWT Bearer token (obtenido vía /api/login/).
    El BFF almacena ese token dentro de su propio JWT como campo 'uat'.
    """

    def __init__(self):
        super().__init__("USUARIOS_URL", "usuarios")

    # ── Públicos (AllowAny) ──

    async def registrar(self, rut: str, email: str, first_name: str, last_name: str, password: str) -> dict:
        return await self.post("/api/usuarios/", {
            "rut": rut,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        })

    async def login(self, rut: str, password: str) -> dict:
        return await self.post("/api/login/", {"rut": rut, "password": password})

    # ── Requieren token de Usuarios (IsAuthenticated) ──

    async def obtener_usuario(self, user_id: int, token: str = None) -> dict:
        return await self.get(f"/api/usuarios/{user_id}/", token=token)

    async def listar_usuarios(self, params: dict = None, token: str = None) -> list:
        resp = await self.get("/api/usuarios/", params=params, token=token)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def actualizar_usuario(self, user_id: int, data: dict, token: str = None) -> dict:
        return await self.patch(f"/api/usuarios/{user_id}/", data=data, token=token)
