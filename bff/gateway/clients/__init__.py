from .base import ServiceClient, RedisCircuitBreaker, request_with_fallback
from .usuarios_client import UsuariosClient
from .logistica_client import LogisticaClient
from .donaciones_client import DonacionesClient
from .necesidades_client import NecesidadesClient

usuarios_client = UsuariosClient()
logistica_client = LogisticaClient()
donaciones_client = DonacionesClient()
necesidades_client = NecesidadesClient()

__all__ = [
    "ServiceClient", "RedisCircuitBreaker", "request_with_fallback",
    "usuarios_client", "logistica_client", "donaciones_client", "necesidades_client",
]
