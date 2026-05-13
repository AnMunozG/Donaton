from .base import ServiceClient, RedisCircuitBreaker, request_with_fallback
from .pago_client import PagoClient
from .notif_client import NotificacionClient
from .donaciones_client import DonacionesClient
from .inventario_client import InventarioClient
from .logistica_client import LogisticaClient
from .catalogos_client import CatalogosClient

pago_client = PagoClient()
notif_client = NotificacionClient()
donaciones_client = DonacionesClient()
inventario_client = InventarioClient()
logistica_client = LogisticaClient()
catalogos_client = CatalogosClient()

__all__ = [
    "ServiceClient", "RedisCircuitBreaker", "request_with_fallback",
    "pago_client", "notif_client", "donaciones_client",
    "inventario_client", "logistica_client", "catalogos_client",
]
