from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from .models import Donacion


class DonacionModelTests(TestCase):
    def test_crear_donacion(self):
        donacion = Donacion.objects.create(
            tipo="Alimentos no perecibles",
            cantidad=500,
            unidad="kg",
            origen="11111111-1",
            centroId="1",
            fecha=date.today(),
            estado="Recibido"
        )
        self.assertEqual(Donacion.objects.count(), 1)
        self.assertEqual(donacion.tipo, "Alimentos no perecibles")
        self.assertEqual(donacion.cantidad, 500)

    def test_timestamps_auto(self):
        donacion = Donacion.objects.create(
            tipo="Ropa", cantidad=10, unidad="cajas",
            origen="22222222-2", centroId="2",
            fecha=date.today(), estado="Pendiente"
        )
        self.assertIsNotNone(donacion.created_at)
        self.assertIsNotNone(donacion.updated_at)

    def test_detalles_json_default(self):
        donacion = Donacion.objects.create(
            tipo="Medicinas", cantidad=100, unidad="unidades",
            origen="33333333-3", centroId="3",
            fecha=date.today(), estado="Recibido"
        )
        self.assertEqual(donacion.detalles, {})

    def test_str_representation(self):
        donacion = Donacion.objects.create(
            tipo="Donación Monetaria", cantidad=1000000, unidad="CLP",
            origen="44444444-4", centroId="1",
            fecha=date.today(), estado="Recibido"
        )
        expected = f"{donacion.idDonacion} - Donación Monetaria"
        self.assertEqual(str(donacion), expected)


class DonacionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Donacion.objects.create(
            tipo="Alimentos", cantidad=500, unidad="kg",
            origen="11111111-1", centroId="1",
            fecha=date.today(), estado="Recibido"
        )
        Donacion.objects.create(
            tipo="Ropa", cantidad=10, unidad="cajas",
            origen="22222222-2", centroId="2",
            fecha=date.today(), estado="Pendiente"
        )

    # --- LISTAR ---

    def test_listar_donaciones(self):
        response = self.client.get('/api/donaciones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filtrar_por_estado(self):
        response = self.client.get('/api/donaciones/', {'estado': 'Recibido'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for d in response.data:
            self.assertEqual(d['estado'], 'Recibido')

    def test_filtrar_por_tipo(self):
        response = self.client.get('/api/donaciones/', {'tipo': 'Ropa'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['tipo'], 'Ropa')

    def test_filtrar_por_centro(self):
        response = self.client.get('/api/donaciones/', {'centro_code': '1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for d in response.data:
            self.assertEqual(d['centroId'], '1')

    # --- CREAR ---

    def test_crear_donacion(self):
        data = {
            "tipo": "Insumos médicos",
            "cantidad": 200,
            "unidad": "unidades",
            "origen": "33333333-3",
            "centroId": "3",
            "fecha": str(date.today()),
            "estado": "Pendiente"
        }
        response = self.client.post('/api/donaciones/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tipo'], "Insumos médicos")
        self.assertEqual(Donacion.objects.count(), 3)

    def test_crear_donacion_sin_campos_obligatorios_falla(self):
        response = self.client.post('/api/donaciones/', {"tipo": "Test"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- OBTENER ---

    def test_obtener_donacion_por_id(self):
        donacion = Donacion.objects.first()
        response = self.client.get(f'/api/donaciones/{donacion.idDonacion}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tipo'], donacion.tipo)

    # --- ACTUALIZAR ---

    def test_actualizar_estado_donacion(self):
        donacion = Donacion.objects.first()
        response = self.client.patch(
            f'/api/donaciones/{donacion.idDonacion}/',
            {"estado": "Entregado"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        donacion.refresh_from_db()
        self.assertEqual(donacion.estado, "Entregado")

    # --- ELIMINAR ---

    def test_eliminar_donacion(self):
        donacion = Donacion.objects.first()
        response = self.client.delete(f'/api/donaciones/{donacion.idDonacion}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Donacion.objects.count(), 1)

    # --- STATS ---

    def test_stats_endpoint(self):
        response = self.client.get('/api/donaciones/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_donaciones', response.data)
        self.assertIn('por_estado', response.data)
        self.assertIn('por_tipo', response.data)
