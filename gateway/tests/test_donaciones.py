import pytest


@pytest.mark.django_db(transaction=True)
class TestHealth:
    async def test_health_endpoint(self, client):
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "servicios" in data
        assert "version" in data


@pytest.mark.django_db(transaction=True)
class TestAuth:
    async def test_login_invalid_returns_401(self, client):
        response = await client.post(
            "/api/auth/login",
            json={"rut": "nonexistent", "password": "wrong"},
        )
        assert response.status_code == 401

    async def test_register_proxies_to_usuarios(self, client, monkeypatch):
        called = []

        async def mock_register(*args, **kwargs):
            called.append(True)
            return {"rut": "12.345.678-9", "email": "test@example.com", "first_name": "Test", "last_name": ""}

        monkeypatch.setattr("gateway.services.auth_service.usuarios_client.registrar", mock_register)

        response = await client.post(
            "/api/auth/register",
            json={
                "rut": "12.345.678-9",
                "nombre": "Test User",
                "email": "test@example.com",
                "password": "testpass123",
            },
        )
        assert response.status_code == 201
        assert len(called) == 1


@pytest.mark.django_db(transaction=True)
class TestEndpointsSinMicroservicio:
    """Endpoints que aún no tienen microservicio deben responder gracefulmente."""

    async def test_list_donaciones_empty(self, client, auth_headers):
        response = await client.get("/api/donaciones", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_necesidades_empty(self, client, auth_headers):
        response = await client.get("/api/necesidades", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_envios_empty(self, client):
        response = await client.get("/api/envios")
        assert response.status_code == 200
        assert response.json() == []
