import pytest


@pytest.mark.django_db(transaction=True)
class TestHealth:
    async def test_health_endpoint(self, client):
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "redis" in data
        assert "servicios" in data or "db" in data
        assert "version" in data


@pytest.mark.django_db(transaction=True)
class TestAuth:
    async def test_register(self, client):
        payload = {
            "rut": "12.345.678-9",
            "nombre": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
        }
        response = await client.post("/api/auth/register", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["rut"] == "12.345.678-9"
        assert data["nombre"] == "Test User"

    async def test_login(self, client):
        await client.post(
            "/api/auth/register",
            json={
                "rut": "98.765.432-1",
                "nombre": "Login Test",
                "email": "login@test.com",
                "password": "pass123",
            },
        )
        response = await client.post(
            "/api/auth/login",
            json={"rut": "98.765.432-1", "password": "pass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data


@pytest.mark.django_db(transaction=True)
class TestDonaciones:
    async def test_list_donaciones(self, client, auth_headers):
        response = await client.get("/api/donaciones", headers=auth_headers)
        assert response.status_code == 200

    async def test_create_donacion_mocked(self, client):
        register_resp = await client.post(
            "/api/auth/register",
            json={
                "rut": "11.222.333-4",
                "nombre": "Donor Test",
                "email": "donor@test.cl",
                "password": "pass123",
            },
        )
        assert register_resp.status_code == 201

        login_resp = await client.post(
            "/api/auth/login",
            json={"rut": "11.222.333-4", "password": "pass123"},
        )
        token = login_resp.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        list_resp = await client.get("/api/donaciones", headers=headers)
        assert list_resp.status_code == 200
