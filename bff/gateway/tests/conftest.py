import pytest
from httpx import ASGITransport, AsyncClient
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
    """Simula un JWT válido con rut para endpoints autenticados."""
    from datetime import datetime, timedelta, timezone
    import jwt
    from django.conf import settings

    payload = {
        "rut": "99.999.999-9",
        "nombre": "Test User",
        "email": "test@test.cl",
        "rol": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    secret = getattr(settings, "JWT_SECRET", settings.SECRET_KEY)
    token = jwt.encode(payload, secret, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
def mock_http_clients(monkeypatch):
    """Mockear todos los clientes HTTP para evitar llamadas reales a microservicios."""

    async def mock_return(*args, **kwargs):
        return {}

    async def mock_list(*args, **kwargs):
        return []

    for path, mock_fn in [
        ("gateway.clients.usuarios_client", mock_return),
        ("gateway.clients.logistica_client", mock_return),
        ("gateway.clients.donaciones_client", mock_return),
    ]:
        monkeypatch.setattr(f"{path}.get", mock_list)
        monkeypatch.setattr(f"{path}.post", mock_return)
        monkeypatch.setattr(f"{path}.put", mock_return)
        monkeypatch.setattr(f"{path}.patch", mock_return)
        monkeypatch.setattr(f"{path}.delete", mock_return)
        monkeypatch.setattr(f"{path}._request", mock_return)
