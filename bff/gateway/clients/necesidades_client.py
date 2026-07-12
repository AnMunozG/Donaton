import time
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .base import ServiceClient


class NecesidadesClient(ServiceClient):
    """Cliente para el microservicio de Necesidades (puerto 8004).

    Se autentica automáticamente creando un JWT de sistema firmado
    con el SECRET_KEY de Necesidades (vía env NECESIDADES_JWT_SECRET).
    """

    def __init__(self):
        super().__init__("NECESIDADES_URL", "necesidades")
        self._system_token = None
        self._token_exp = 0.0

    def _get_system_token(self) -> str:
        now_ts = time.time()
        if self._system_token and now_ts < self._token_exp:
            return self._system_token

        secret = getattr(settings, "NECESIDADES_JWT_SECRET", "")
        if not secret:
            return ""

        now = datetime.now(timezone.utc)
        system_user_id = getattr(settings, "NECESIDADES_SYSTEM_USER_ID", 1)
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

    async def listar_necesidades(self, params: dict = None) -> list:
        resp = await self.get("/api/necesidades/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_necesidad(self, code: str) -> dict:
        return await self.get(f"/api/necesidades/{code}/")

    async def crear_necesidad(self, data: dict) -> dict:
        return await self.post("/api/necesidades/", data)

    async def actualizar_necesidad(self, code: str, data: dict) -> dict:
        return await self.patch(f"/api/necesidades/{code}/", data)

    async def eliminar_necesidad(self, code: str) -> dict:
        return await self.delete(f"/api/necesidades/{code}/")
