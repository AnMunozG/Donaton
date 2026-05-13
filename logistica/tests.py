from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Producto, CentroAcopio, Inventario

class LogisticaTests(TestCase):
    def setUp(self):
        """Configuración inicial usando los nombres de campos de tus modelos"""
        self.client = APIClient()
        
        # Crear usuarios para pruebas de seguridad
        self.admin_user = User.objects.create_superuser(
            username='admin', password='password123', email='admin@test.com'
        )
        self.normal_user = User.objects.create_user(
            username='user', password='password123'
        )
        
        # Crear Centro de Acopio 
        self.centro = CentroAcopio.objects.create(
            nombre="Centro Test Santiago",
            direccion="Calle Falsa 123",
            capacidadTotal=5000,
            capacidadUsada=0
        )
        
        # Crear Producto
        self.producto = Producto.objects.create(
            nombre="Arroz",
            categoria="ALIMENTOS",
            unidadMedida="kg"
        )

    # --- PRUEBAS DE SEGURIDAD ---

    def test_acceso_denegado_sin_token(self):
        response = self.client.get('/api/productos/') 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_puede_crear_producto(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nombre": "Agua Mineral", 
            "categoria": "ALIMENTOS",
            "unidadMedida": "unidades"
        }
        response = self.client.post('/api/productos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # --- PRUEBAS DE MODELOS ---

    def test_verificar_campos_modelo(self):
        """Verifica que los datos se guardaron con los nombres camelCase"""
        centro = CentroAcopio.objects.get(nombre="Centro Test Santiago")
        self.assertEqual(centro.capacidadTotal, 5000)
        
        producto = Producto.objects.get(nombre="Arroz")
        self.assertEqual(producto.unidadMedida, "kg")

# --- TEST DE RELACIONES (PRODUCTO + CENTRO = INVENTARIO) ---

    def test_crear_item_inventario(self):
        """Verifica que se puede asociar un producto a un centro con una cantidad"""
        self.client.force_authenticate(user=self.admin_user)
        
        # Datos del inventario (Relacionando lo creado en setUp)
        data = {
            "producto": self.producto.id,
            "centro": self.centro.id,
            "cantidad": 50.5
        }
        response = self.client.post('/api/inventario/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Inventario.objects.count(), 1)

    # --- TEST DE VALIDACIÓN DE DATOS ---

    def test_crear_producto_sin_nombre_falla(self):
        """Verifica que el serializer valida campos obligatorios"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "categoria": "ROPA" 
            # Falta el nombre
        }
        response = self.client.post('/api/productos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('nombre', response.data) # El error debe mencionar el campo 'nombre'