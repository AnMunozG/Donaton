from django.conf import settings
from .base import RedisCircuitBreaker, _request_with_cb

pago_cb = RedisCircuitBreaker("pagos_gateway")


async def cobrar(monto: float, origen: str, descripcion: str = "") -> dict:
    return await _request_with_cb(
        pago_cb,
        getattr(settings, "PAGOS_URL", None),
        {"monto": monto, "origen": origen, "descripcion": descripcion},
        {"estado": "pendiente_confirmacion", "monto": monto, "origen": origen},
    )


async def reembolsar(monto: float, origen: str) -> dict:
    url = getattr(settings, "PAGOS_URL", None)
    if not url:
        return {"estado": "simulado", "monto": monto}
    return await _request_with_cb(
        pago_cb,
        f"{url}/reembolso",
        {"monto": monto, "origen": origen},
        {"estado": "pendiente"},
    )
