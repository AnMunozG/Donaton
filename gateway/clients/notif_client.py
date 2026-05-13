from django.conf import settings
from .base import RedisCircuitBreaker, _request_with_cb

notif_cb = RedisCircuitBreaker("notificaciones")


async def enviar_email(destino: str, asunto: str, mensaje: str) -> dict:
    url = getattr(settings, "NOTIFICACIONES_URL", None)
    if not url:
        return {"estado": "simulado"}
    return await _request_with_cb(
        notif_cb,
        f"{url}/email",
        {"destino": destino, "asunto": asunto, "mensaje": mensaje},
        {"estado": "pendiente"},
    )


async def enviar_sms(destino: str, mensaje: str) -> dict:
    url = getattr(settings, "NOTIFICACIONES_URL", None)
    if not url:
        return {"estado": "simulado"}
    return await _request_with_cb(
        notif_cb,
        f"{url}/sms",
        {"destino": destino, "mensaje": mensaje},
        {"estado": "pendiente"},
    )
