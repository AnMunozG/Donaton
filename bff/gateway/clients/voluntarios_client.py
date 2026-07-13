import time
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .base import ServiceClient


class VoluntariosClient(ServiceClient):
    """Cliente para el microservicio de Voluntarios (puerto 8005).

    Se autentica automáticamente creando un JWT de sistema firmado
    con el SECRET_KEY de Voluntarios (vía env VOLUNTARIOS_JWT_SECRET).
    """

    def __init__(self):
        super().__init__("VOLUNTARIOS_URL", "voluntarios")
        self._system_token = None
        self._token_exp = 0.0

    def _get_system_token(self) -> str:
        now_ts = time.time()
        if self._system_token and now_ts < self._token_exp:
            return self._system_token

        secret = getattr(settings, "VOLUNTARIOS_JWT_SECRET", "")
        if not secret:
            return ""

        now = datetime.now(timezone.utc)
        system_user_id = getattr(settings, "VOLUNTARIOS_SYSTEM_USER_ID", 1)
        payload = {
            "token_type": "access",
            "exp": now + timedelta(hours=24),
            "iat": now,
            "jti": f"system-{system_user_id}-{int(now.timestamp())}",
            "user_id": system_user_id,
        }
        self._system_token = jwt.encode(payload, secret, algorithm="HS256")
        self._token_exp = (now + timedelta(hours=24)).timestamp()
        return self._system_token

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        token = kwargs.pop("token", None) or self._get_system_token()
        return await super()._request(method, path, token=token, **kwargs)

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

    async def listar_horas(self, code: str, centro_id: str = None) -> dict:
        params = {}
        if centro_id:
            params["centro_id"] = centro_id
        return await self.get(f"/api/voluntarios/{code}/horas/", params=params or None)

    async def registrar_horas(self, code: str, data: dict) -> dict:
        return await self.post(f"/api/voluntarios/{code}/registrar-horas/", data)

    async def obtener_voluntario_por_rut(self, rut: str) -> dict | None:
        resultados = await self.listar_voluntarios(params={"rut": rut})
        if isinstance(resultados, list) and len(resultados) > 0:
            return resultados[0]
        return None

    async def listar_voluntario_centros(self, params: dict = None) -> list:
        resp = await self.get("/api/voluntario-centros/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def crear_voluntario_centro(self, data: dict) -> dict:
        return await self.post("/api/voluntario-centros/", data)

    async def actualizar_voluntario_centro(self, code: str, data: dict) -> dict:
        return await self.patch(f"/api/voluntario-centros/{code}/", data)

    async def eliminar_voluntario_centro(self, code: str) -> dict:
        return await self.delete(f"/api/voluntario-centros/{code}/")

    async def listar_asignaciones(self, params: dict = None) -> list:
        resp = await self.get("/api/asignaciones/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def crear_asignacion(self, data: dict) -> dict:
        return await self.post("/api/asignaciones/", data)

    async def crear_notificacion(self, data: dict) -> dict:
        return await self.post("/api/notificaciones/", data)

    async def listar_notificaciones(self, params: dict = None) -> list:
        resp = await self.get("/api/notificaciones/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def marcar_notificacion_leida(self, notif_id: str) -> dict:
        return await self.patch(f"/api/notificaciones/{notif_id}/marcar-leida/", {})
