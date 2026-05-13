import json
from datetime import datetime, timezone
from typing import Callable, Any

from django.conf import settings

try:
    import redis.asyncio as aioredis
except ImportError:
    aioredis = None


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
            if not aioredis:
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

    async def call(self, fn: Callable, *args, **kwargs) -> Any:
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


async def _request_with_cb(cb: RedisCircuitBreaker, url: str, data: dict, fallback: dict) -> dict:
    """Helper para clients: llama con circuit breaker, retorna fallback si falla."""
    import httpx, logging
    logger = logging.getLogger(__name__)

    if not url:
        logger.info(f"URL no configurada para {cb.name}, simulando")
        return {"estado": "simulado", **data}

    async def _do():
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=data)
            resp.raise_for_status()
            return resp.json()

    try:
        return await cb.call(_do)
    except Exception as e:
        logger.warning(f"{cb.name} falló: {e}")
        return fallback
