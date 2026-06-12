from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Usuario


class UsuariosTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Usar un RUT distinto al del admin creado por migracion 0003
        self.test_rut = '22222222-2'
        self.test_user = Usuario.objects.create_user(
            rut=self.test_rut,
            username=self.test_rut,
            password='testpass123',
            email='test@test.cl',
            first_name='Test',
        )

    # --- REGISTRO ---

    def test_registrar_usuario(self):
        data = {
            "rut": "12345678-5",
            "email": "nuevo@test.cl",
            "first_name": "Nuevo",
            "password": "pass1234"
        }
        response = self.client.post('/api/usuarios/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registrar_rut_duplicado_rechazado(self):
        # Crear primero
        data = {
            "rut": "1111112-2",
            "email": "primero@test.cl",
            "first_name": "Primero",
            "password": "pass1234"
        }
        response = self.client.post('/api/usuarios/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Intentar duplicar
        response = self.client.post('/api/usuarios/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- LOGIN ---

    def test_login_exitoso(self):
        response = self.client.post('/api/login/', {
            "rut": self.test_rut,
            "password": "testpass123"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_fallido(self):
        response = self.client.post('/api/login/', {
            "rut": self.test_rut,
            "password": "wrongpass"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- SEGURIDAD ---

    def test_listar_usuarios_sin_token_rechazado(self):
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_usuario_autenticado_puede_listar(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtener_perfil_propio(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(f'/api/usuarios/{self.test_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rut'], self.test_rut)

    # --- MODELO ---

    def test_campos_usuario(self):
        self.assertEqual(self.test_user.rut, self.test_rut)
        self.assertEqual(self.test_user.email, 'test@test.cl')
        self.assertTrue(self.test_user.is_active)
