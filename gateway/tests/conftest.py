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
