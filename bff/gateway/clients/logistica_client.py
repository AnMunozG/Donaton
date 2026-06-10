import time
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .base import ServiceClient


class LogisticaClient(ServiceClient):
    """Cliente para el microservicio de Logística (puerto 8001).

    Se autentica automáticamente creando un JWT de sistema firmado
    con el SECRET_KEY de Logística (vía env LOGISTICA_JWT_SECRET).
    Esto evita modificar Logística — acepta el token como si fuera
    generado por su propio TokenObtainPairView.
    """

    def __init__(self):
        super().__init__("LOGISTICA_URL", "logistica")
        self._system_token = None
        self._token_exp = 0.0

    def _get_system_token(self) -> str:
        now_ts = time.time()
        if self._system_token and now_ts < self._token_exp:
            return self._system_token

        secret = getattr(settings, "LOGISTICA_JWT_SECRET", "")
        if not secret:
            return ""

        now = datetime.now(timezone.utc)
        system_user_id = getattr(settings, "LOGISTICA_SYSTEM_USER_ID", 1)
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
        if method.upper() == "GET":
            token = kwargs.pop("token", None)
        else:
            token = kwargs.pop("token", None) or self._get_system_token()
            
        return await super()._request(method, path, token=token, **kwargs)

    # ── Centros ──

    async def listar_centros(self, params: dict = None) -> list:
        resp = await self.get("/api/centros/", params=params)
        return resp if isinstance(resp, list) else resp.get("results", [])

    async def obtener_centro(self, id_: int) -> dict:
        return await self.get(f"/api/centros/{id_}/")

    async def crear_centro(self, data: dict) -> dict:
        return await self.post("/api/centros/", data)

    async def actualizar_centro(self, id_: int, data: dict) -> dict:
        return await self.patch(f"/api/centros/{id_}/", data)

    async def eliminar_centro(self, id_: int) -> dict:
        return await self.delete(f"/api/centros/{id_}/")
