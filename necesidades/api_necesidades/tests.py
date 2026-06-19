from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Necesidad

class NecesidadAPITests(APITestCase):

    def setUp(self):
        # Esta función corre antes de cada prueba para tener datos base en la BD de pruebas
        self.url_lista = reverse('necesidad-list')  # Apunta a /api/necesidades/v1/
        
        self.necesidad_ejemplo = Necesidad.objects.create(
            centro_acopio_id=1,
            titulo="Cajas de Leche Entera",
            descripcion="Para el desayuno de los niños del sector campamento.",
            categoria="ALIMENTOS",
            cantidad_requerida=100,
            unidad_medida="cajas",
            solicitante_nombre="Comedor Abierto",
            solicitante_contacto="contacto@comedor.cl"
        )
        # Ruta para pruebas que requieren un ID específico (/api/necesidades/v1/1/)
        self.url_detalle = reverse('necesidad-detail', args=[self.necesidad_ejemplo.id])

    # -------------------------------------------------------------------------
    # BLOQUE 1: PRUEBAS DE CREACIÓN Y VALIDACIÓN (FORMULARIO)
    # -------------------------------------------------------------------------

    def test_01_crear_necesidad_exitosamente(self):
        """1. Verifica que el formulario guarde una necesidad válida"""
        data = {
            "centro_acopio_id": 2,
            "titulo": "Mascarillas Clínicas",
            "descripcion": "Urgente para el puesto de salud avanzado.",
            "categoria": "SALUD",
            "cantidad_requerida": 500,
            "unidad_medida": "unidades",
            "solicitante_nombre": "Cruz Roja Local",
            "solicitante_contacto": "+56987654321"
        }
        response = self.client.post(self.url_lista, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Necesidad.objects.count(), 2)
        self.assertEqual(response.data['estado'], 'Pendiente')

    def test_02_error_cuando_cantidad_requerida_es_cero_o_negativa(self):
        """2. El Serializer debe rechazar formularios con cantidades absurdas"""
        data = {
            "centro_acopio_id": 1,
            "titulo": "Frazadas de abrigo",
            "descripcion": "Para bajas temperaturas.",
            "categoria": "ROPA",
            "cantidad_requerida": 0,  # <--- Invalido
            "unidad_medida": "unidades",
            "solicitante_nombre": "Albergue Central",
            "solicitante_contacto": "albergue@donaton.cl"
        }
        response = self.client.post(self.url_lista, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cantidad_requerida', response.data)

    def test_03_error_cuando_titulo_es_muy_corto(self):
        """3. Evita que envíen formularios con títulos basura como 'hola' o 'ayuda'"""
        data = {
            "centro_acopio_id": 1,
            "titulo": "Agua",  # <--- Muy corto (menos de 5 letras)
            "descripcion": "Se necesitan bidones de agua.",
            "categoria": "ALIMENTOS",
            "cantidad_requerida": 10,
            "solicitante_nombre": "Vecinos Unidos",
            "solicitante_contacto": "12345"
        }
        response = self.client.post(self.url_lista, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_04_error_id_centro_acopio_invalido(self):
        """4. Asegura que el ID de logística sea un número entero positivo válido"""
        data = {
            "centro_acopio_id": 0,  # <--- ID inexistente o inválido
            "titulo": "Herramientas de remoción",
            "descripcion": "Palas y picotas.",
            "categoria": "OTROS",
            "cantidad_requerida": 5,
            "solicitante_nombre": "Bomberos",
            "solicitante_contacto": "132"
        }
        response = self.client.post(self.url_lista, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------------------------
    # BLOQUE 2: PRUEBAS DE LECTURA Y FILTRADO (FRONTEND / BFF)
    # -------------------------------------------------------------------------

    def test_05_obtener_lista_de_necesidades(self):
        """5. El frontend debe poder listar todas las necesidades activas"""
        response = self.client.get(self.url_lista)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)