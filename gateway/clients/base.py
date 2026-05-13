import json, logging
from datetime import datetime, timezone
from typing import Any, Optional

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class ServiceClient:
    """Cliente HTTP base con circuit breaker integrado para consumir microservicios."""

    def __init__(self, base_url_key: str, service_name: str, timeout: int = 10):
        self.base_url = getattr(settings, base_url_key, "")
        self.service_name = service_name
        self.timeout = timeout

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        if not self.base_url:
            return {"estado": "simulado", "service": self.service_name, "path": path}

        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.request(method, url, **kwargs)
            resp.raise_for_status()
            return resp.json()

    async def get(self, path: str, params: Optional[dict] = None) -> dict:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, data: Optional[dict] = None) -> dict:
        return await self._request("POST", path, json=data or {})

    async def put(self, path: str, data: Optional[dict] = None) -> dict:
        return await self._request("PUT", path, json=data or {})

    async def patch(self, path: str, data: Optional[dict] = None) -> dict:
        return await self._request("PATCH", path, json=data or {})

    async def delete(self, path: str) -> dict:
        return await self._request("DELETE", path)


class RedisCircuitBreaker:
    def __init__(self, name: str, failure_threshold: int = 5, recovery_timeout: int = 30, half_open_max_calls: int = 3):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self._redis = None
        self._local_half_count = 0

    async def _get_redis(self):
        if self._redis is None:
            redis_url = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")
            try:
                import redis.asyncio as aioredis
            except ImportError:
                raise RuntimeError("redis[asyncio] no está instalado")
            self._redis = aioredis.from_url(redis_url, decode_responses=True)
        return self._redis

    async def _get_state(self):
        r = await self._get_redis()
        raw = await r.get(f"cb:{self.name}")
        if not raw:
            return {"state": "closed", "failures": 0, "last_failure_ts": 0.0}
        return json.loads(raw)

    async def _save_state(self, s):
        r = await self._get_redis()
        await r.set(f"cb:{self.name}", json.dumps(s))

    async def call(self, fn, *args, **kwargs) -> Any:
        state = await self._get_state()
        now = datetime.now(timezone.utc).timestamp()

        if state["state"] == "open":
            if now - state["last_failure_ts"] < self.recovery_timeout:
                raise Exception(f"Circuit breaker '{self.name}' OPEN")
            state["state"] = "half-open"
            self._local_half_count = 0
            await self._save_state(state)

        if state["state"] == "half-open":
            if self._local_half_count >= self.half_open_max_calls:
                raise Exception(f"Circuit breaker '{self.name}' HALF-OPEN")
            self._local_half_count += 1

        try:
            result = await fn(*args, **kwargs)
            await self._save_state({"state": "closed", "failures": 0, "last_failure_ts": 0.0})
            self._local_half_count = 0
            return result
        except Exception as e:
            state["failures"] += 1
            state["last_failure_ts"] = now
            if state["failures"] >= self.failure_threshold:
                state["state"] = "open"
            await self._save_state(state)
            raise

    async def get_state_name(self) -> str:
        return (await self._get_state())["state"]


async def request_with_fallback(client: ServiceClient, method: str, path: str, fallback: dict, **kwargs) -> dict:
    try:
        return await client._request(method, path, **kwargs)
    except Exception as e:
        logger.warning(f"{client.service_name}/{path} falló: {e}")
        return fallback
