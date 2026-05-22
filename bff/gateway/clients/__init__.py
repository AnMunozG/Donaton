from .base import ServiceClient, RedisCircuitBreaker, request_with_fallback
from .usuarios_client import UsuariosClient
from .logistica_client import LogisticaClient
from .pago_client import PagoClient
from .notif_client import NotificacionClient
from .catalogos_client import CatalogosClient

usuarios_client = UsuariosClient()
logistica_client = LogisticaClient()
pago_client = PagoClient()
notif_client = NotificacionClient()
catalogos_client = CatalogosClient()

__all__ = [
    "ServiceClient", "RedisCircuitBreaker", "request_with_fallback",
    "usuarios_client", "logistica_client",
    "pago_client", "notif_client", "catalogos_client",
]
