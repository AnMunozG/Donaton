from .base import ServiceClient, RedisCircuitBreaker, request_with_fallback
from .usuarios_client import UsuariosClient
from .logistica_client import LogisticaClient
from .donaciones_client import DonacionesClient

usuarios_client = UsuariosClient()
logistica_client = LogisticaClient()
donaciones_client = DonacionesClient()

__all__ = [
    "ServiceClient", "RedisCircuitBreaker", "request_with_fallback",
    "usuarios_client", "logistica_client", "donaciones_client",
]
