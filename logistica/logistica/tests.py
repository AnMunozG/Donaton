from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import CentroAcopio


class LogisticaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin', password='password123', email='admin@test.com'
        )
        self.centro = CentroAcopio.objects.create(
            nombre="Centro Test Santiago",
            region="Metropolitana",
            capacidadTotal=5000,
            capacidadUsada=1000,
            estado="Activo"
        )

    # --- SEGURIDAD ---

    def test_listar_centros_sin_token(self):
        response = self.client.get('/api/centros/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_centro_sin_token_rechazado(self):
        data = {"nombre": "Nuevo", "region": "Valparaíso", "capacidadTotal": 1000, "capacidadUsada": 0}
        response = self.client.post('/api/centros/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_puede_crear_centro(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nombre": "Centro Viña",
            "region": "Valparaíso",
            "capacidadTotal": 3000,
            "capacidadUsada": 500,
            "estado": "Activo"
        }
        response = self.client.post('/api/centros/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], "Centro Viña")

    def test_admin_puede_eliminar_centro(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/centros/{self.centro.idCentro}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CentroAcopio.objects.filter(idCentro=self.centro.idCentro).exists())

    # --- MODELOS ---

    def test_campos_camelcase(self):
        centro = CentroAcopio.objects.get(nombre="Centro Test Santiago")
        self.assertEqual(centro.capacidadTotal, 5000)
        self.assertEqual(centro.capacidadUsada, 1000)
        self.assertEqual(centro.estado, "Activo")

    def test_inventario_json_default(self):
        self.assertEqual(self.centro.inventario, [])

    # --- VALIDACIÓN ---

    def test_crear_centro_sin_nombre_falla(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"region": "Metropolitana", "capacidadTotal": 1000, "capacidadUsada": 0}
        response = self.client.post('/api/centros/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_centro_sin_capacidad_falla(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {"nombre": "Test", "region": "Metropolitana"}
        response = self.client.post('/api/centros/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- OPERACIONES ---

    def test_actualizar_centro(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            f'/api/centros/{self.centro.idCentro}/',
            {"capacidadUsada": 2000},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.centro.refresh_from_db()
        self.assertEqual(self.centro.capacidadUsada, 2000)

    def test_obtener_centro_por_id(self):
        response = self.client.get(f'/api/centros/{self.centro.idCentro}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], "Centro Test Santiago")
