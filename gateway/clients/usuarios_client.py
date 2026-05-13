from .base import ServiceClient


class UsuariosClient(ServiceClient):
    """Cliente para el microservicio de Usuarios (puerto 8000).

    Endpoints:
      POST   /api/usuarios/        — registro
      GET    /api/usuarios/         — listar (requiere auth)
      GET    /api/usuarios/{id}/    — detalle
      PUT    /api/usuarios/{id}/    — actualizar
      POST   /api/login/            — obtener JWT (access + refresh)
      POST   /api/token/refresh/    — refrescar access token
    """

    def __init__(self):
        super().__init__("USUARIOS_URL", "usuarios")

    # ── Registro ──

    async def registrar(self, rut: str, email: str, first_name: str, last_name: str, password: str) -> dict:
        return await self.post("/api/usuarios/", {
            "rut": rut,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        })

    # ── Login ──

    async def login(self, rut: str, password: str) -> dict:
        return await self.post("/api/login/", {"rut": rut, "password": password})

    async def refresh_token(self, refresh: str) -> dict:
        return await self.post("/api/token/refresh/", {"refresh": refresh})

    # ── Perfil ──

    async def obtener_usuario(self, user_id: int) -> dict:
        return await self.get(f"/api/usuarios/{user_id}/")

    async def listar_usuarios(self, params: dict = None) -> list:
        resp = await self.get("/api/usuarios/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])
