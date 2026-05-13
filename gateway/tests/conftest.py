import pytest
from httpx import ASGITransport, AsyncClient
from asgiref.sync import sync_to_async

from config.asgi import application


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        pass


@pytest.fixture
async def client():
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def auth_headers(client):
    from gateway.models import Cuenta
    from gateway.services.auth_service import _create_token

    @sync_to_async
    def create_cuenta():
        cuenta, _ = Cuenta.objects.get_or_create(
            rut="99.999.999-9",
            defaults={
                "nombre": "Test User",
                "email": "test@test.cl",
                "password": "pbkdf2_sha256$...",
                "rol": "admin",
            },
        )
        return cuenta

    cuenta = await create_cuenta()
    token = _create_token(cuenta)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def mock_http_clients(monkeypatch):
    """Mockear todos los clientes HTTP para que no hagan llamadas reales."""

    async def mock_list(*args, **kwargs):
        return []

    async def mock_get(*args, **kwargs):
        return {}

    async def mock_post(*args, **kwargs):
        return {}

    async def mock_put(*args, **kwargs):
        return {}

    async def mock_patch(*args, **kwargs):
        return {}

    for client_path in [
        "gateway.clients.donaciones_client",
        "gateway.clients.inventario_client",
        "gateway.clients.logistica_client",
        "gateway.clients.catalogos_client",
        "gateway.clients.pago_client",
        "gateway.clients.notif_client",
    ]:
        monkeypatch.setattr(f"{client_path}.get", mock_get)
        monkeypatch.setattr(f"{client_path}.post", mock_post)
        monkeypatch.setattr(f"{client_path}.put", mock_put)
        monkeypatch.setattr(f"{client_path}.patch", mock_patch)
        monkeypatch.setattr(f"{client_path}._request", mock_get)
