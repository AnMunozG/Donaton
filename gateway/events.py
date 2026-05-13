"""
Bus de eventos asíncrono para comunicación entre el BFF y los microservicios.

Usa Redis pub/sub como transporte. En producción podría reemplazarse por
RabbitMQ, Amazon SQS, Google Pub/Sub, etc.
"""
import json, logging
from typing import Callable, Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class EventBus:
    """Permite publicar y suscribirse a eventos de dominio de forma asíncrona."""

    def __init__(self):
        self._redis = None
        self._pubsub = None

    async def _get_redis(self):
        redis_url = getattr(settings, "REDIS_URL", None)
        if not redis_url:
            return None
        if self._redis is None:
            try:
                import redis.asyncio as aioredis
                self._redis = aioredis.from_url(redis_url, decode_responses=True)
            except ImportError:
                logger.warning("redis[asyncio] no instalado, eventos deshabilitados")
                return None
        return self._redis

    async def publish(self, channel: str, event: dict):
        r = await self._get_redis()
        if not r:
            logger.info(f"[EVENTO simulado] canal={channel} evento={event}")
            return
        payload = json.dumps(event)
        await r.publish(channel, payload)
        logger.info(f"[EVENTO publicado] canal={channel} evento={event.get('type')}")

    async def subscribe(self, channel: str, handler: Callable):
        r = await self._get_redis()
        if not r:
            logger.warning(f"Redis no disponible, no se puede suscribir a {channel}")
            return
        self._pubsub = r.pubsub()
        await self._pubsub.subscribe(channel)
        logger.info(f"Suscrito a canal {channel}")
        async for message in self._pubsub.listen():
            if message["type"] == "message":
                try:
                    event = json.loads(message["data"])
                    await handler(event)
                except Exception as e:
                    logger.error(f"Error manejando evento en {channel}: {e}")


# Singleton del bus de eventos
event_bus = EventBus()


# ── Eventos de dominio ──

async def publish_donacion_creada(donacion_code: str, tipo: str, cantidad: float, centro_code: str, origen: str):
    await event_bus.publish("donaciones", {
        "type": "donacion.creada",
        "data": {
            "code": donacion_code,
            "tipo": tipo,
            "cantidad": cantidad,
            "centro_code": centro_code,
            "origen": origen,
        },
    })


async def publish_donacion_estado_cambiado(donacion_code: str, estado_anterior: str, estado_nuevo: str):
    await event_bus.publish("donaciones", {
        "type": "donacion.estado_cambiado",
        "data": {"code": donacion_code, "estado_anterior": estado_anterior, "estado_nuevo": estado_nuevo},
    })


async def publish_necesidad_creada(necesidad_code: str, centro_code: str, tipo_recurso: str, cantidad: float):
    await event_bus.publish("necesidades", {
        "type": "necesidad.creada",
        "data": {"code": necesidad_code, "centro_code": centro_code, "tipo_recurso": tipo_recurso, "cantidad": cantidad},
    })


async def publish_necesidad_activada(necesidad_code: str, centro_code: str):
    await event_bus.publish("necesidades", {
        "type": "necesidad.activada",
        "data": {"code": necesidad_code, "centro_code": centro_code},
    })


async def publish_centro_actualizado(centro_code: str, estado: str):
    await event_bus.publish("inventario", {
        "type": "centro.actualizado",
        "data": {"code": centro_code, "estado": estado},
    })


async def publish_envio_creado(envio_code: str, centro_code: str, destino: str):
    await event_bus.publish("logistica", {
        "type": "envio.creado",
        "data": {"code": envio_code, "centro_code": centro_code, "destino": destino},
    })
