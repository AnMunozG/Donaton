from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Voluntario, RegistroHoras, AsignacionVoluntario


class VoluntarioModelTests(TestCase):

    def setUp(self):
        self.voluntario = Voluntario.objects.create(
            rut="11111111-1",
            disponibilidad="diaria",
            habilidades=["carga", "conduccion"],
            centro_preferido="1",
            estado="activo",
        )

    def test_str_representation(self):
        self.assertIn("11111111-1", str(self.voluntario))
        self.assertIn("Activo", str(self.voluntario))

    def test_horas_acumuladas_sin_registros(self):
        self.assertEqual(self.voluntario.horas_acumuladas, 0)

    def test_horas_acumuladas_con_registros(self):
        RegistroHoras.objects.create(
            voluntario=self.voluntario, horas=5, registrado_por_rut="22222222-2"
        )
        RegistroHoras.objects.create(
            voluntario=self.voluntario, horas=3, registrado_por_rut="22222222-2"
        )
        self.voluntario.refresh_from_db()
        self.assertEqual(self.voluntario.horas_acumuladas, 8)

    def test_activo_property(self):
        self.assertTrue(self.voluntario.activo)
        self.voluntario.estado = "inactivo"
        self.voluntario.save()
        self.assertFalse(self.voluntario.activo)


class RegistroHorasModelTests(TestCase):

    def setUp(self):
        self.voluntario = Voluntario.objects.create(
            rut="11111111-1", estado="activo"
        )
        self.registro = RegistroHoras.objects.create(
            voluntario=self.voluntario,
            horas=4,
            descripcion="Ayuda en carga",
            registrado_por_rut="22222222-2",
        )

    def test_str_representation(self):
        s = str(self.registro)
        self.assertIn("4h", s)
        self.assertIn("11111111-1", s)


class AsignacionVoluntarioModelTests(TestCase):

    def setUp(self):
        self.voluntario = Voluntario.objects.create(
            rut="11111111-1", estado="activo"
        )
        self.asignacion = AsignacionVoluntario.objects.create(
            voluntario=self.voluntario,
            necesidad_id=1,
            estado="asignado",
        )

    def test_str_representation(self):
        s = str(self.asignacion)
        self.assertIn("11111111-1", s)
        self.assertIn("Necesidad #1", s)
        self.assertIn("asignado", s)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            AsignacionVoluntario.objects.create(
                voluntario=self.voluntario,
                necesidad_id=1,
                estado="propuesto",
            )


class VoluntarioSerializerTests(TestCase):

    def setUp(self):
        self.voluntario = Voluntario.objects.create(
            rut="11111111-1",
            disponibilidad="semanal",
            habilidades=["enfermeria"],
            centro_preferido="2",
            estado="pendiente",
        )

    def test_read_only_fields(self):
        from .serializers import VoluntarioSerializer
        serializer = VoluntarioSerializer(self.voluntario)
        data = serializer.data
        self.assertIn("id", data)
        self.assertIn("fecha_registro", data)
        self.assertIn("horas_acumuladas", data)


class RegistroHorasSerializerTests(TestCase):

    def setUp(self):
        self.voluntario = Voluntario.objects.create(
            rut="11111111-1", estado="activo"
        )

    def test_horas_cero_rechazado(self):
        from .serializers import RegistroHorasSerializer
        data = {"voluntario": self.voluntario.id, "horas": 0, "registrado_por_rut": "22222222-2"}
        serializer = RegistroHorasSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("horas", serializer.errors)

    def test_horas_negativas_rechazado(self):
        from .serializers import RegistroHorasSerializer
        data = {"voluntario": self.voluntario.id, "horas": -5, "registrado_por_rut": "22222222-2"}
        serializer = RegistroHorasSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_horas_mayor_24_rechazado(self):
        from .serializers import RegistroHorasSerializer
        data = {"voluntario": self.voluntario.id, "horas": 25, "registrado_por_rut": "22222222-2"}
        serializer = RegistroHorasSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_horas_valida(self):
        from .serializers import RegistroHorasSerializer
        data = {"voluntario": self.voluntario.id, "horas": 8, "registrado_por_rut": "22222222-2"}
        serializer = RegistroHorasSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class VoluntarioViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.vol1 = Voluntario.objects.create(
            rut="11111111-1",
            disponibilidad="diaria",
            habilidades=["carga", "conduccion"],
            centro_preferido="1",
            estado="activo",
        )
        self.vol2 = Voluntario.objects.create(
            rut="22222222-2",
            disponibilidad="semanal",
            habilidades=["enfermeria"],
            centro_preferido="2",
            estado="pendiente",
        )

    def test_listar_voluntarios(self):
        response = self.client.get("/api/voluntarios/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_crear_voluntario(self):
        data = {
            "rut": "33333333-3",
            "disponibilidad": "fines_semana",
            "habilidades": ["cocina"],
            "centro_preferido": "1",
        }
        response = self.client.post("/api/voluntarios/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Voluntario.objects.count(), 3)

    def test_filtrar_por_estado(self):
        response = self.client.get("/api/voluntarios/", {"estado": "activo"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["rut"], "11111111-1")

    def test_filtrar_por_disponibilidad(self):
        response = self.client.get("/api/voluntarios/", {"disponibilidad": "semanal"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_por_centro(self):
        response = self.client.get("/api/voluntarios/", {"centro_preferido": "1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_por_habilidad(self):
        response = self.client.get("/api/voluntarios/", {"habilidad": "enfermeria"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["rut"], "22222222-2")

    def test_filtrar_por_rut(self):
        response = self.client.get("/api/voluntarios/", {"rut": "11111111-1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_por_activo_true(self):
        response = self.client.get("/api/voluntarios/", {"activo": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_por_activo_false(self):
        response = self.client.get("/api/voluntarios/", {"activo": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_voluntario_por_id(self):
        response = self.client.get(f"/api/voluntarios/{self.vol1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rut"], "11111111-1")

    def test_actualizar_voluntario(self):
        data = {"disponibilidad": "emergencia", "habilidades": ["carga", "conduccion", "primeros_auxilios"]}
        response = self.client.patch(f"/api/voluntarios/{self.vol1.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vol1.refresh_from_db()
        self.assertEqual(self.vol1.disponibilidad, "emergencia")

    def test_eliminar_voluntario(self):
        response = self.client.delete(f"/api/voluntarios/{self.vol2.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Voluntario.objects.count(), 1)


class RegistrarHorasTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.voluntario = Voluntario.objects.create(
            rut="11111111-1", estado="activo"
        )

    def test_registrar_horas_exitoso(self):
        url = f"/api/voluntarios/{self.voluntario.id}/registrar-horas/"
        data = {"horas": 5, "descripcion": "Ayuda en carga", "registrado_por_rut": "22222222-2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RegistroHoras.objects.count(), 1)

    def test_registrar_horas_cero_rechazado(self):
        url = f"/api/voluntarios/{self.voluntario.id}/registrar-horas/"
        data = {"horas": 0, "descripcion": "Test", "registrado_por_rut": "22222222-2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registrar_horas_negativas_rechazado(self):
        url = f"/api/voluntarios/{self.voluntario.id}/registrar-horas/"
        data = {"horas": -3, "descripcion": "Test", "registrado_por_rut": "22222222-2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registrar_horas_mayor_24_rechazado(self):
        url = f"/api/voluntarios/{self.voluntario.id}/registrar-horas/"
        data = {"horas": 25, "descripcion": "Test", "registrado_por_rut": "22222222-2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registrar_horas_sin_rut_rechazado(self):
        url = f"/api/voluntarios/{self.voluntario.id}/registrar-horas/"
        data = {"horas": 4, "descripcion": "Test", "registrado_por_rut": ""}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registrar_horas_texto_rechazado(self):
        url = f"/api/voluntarios/{self.voluntario.id}/registrar-horas/"
        data = {"horas": "abc", "descripcion": "Test", "registrado_por_rut": "22222222-2"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_horas_voluntario(self):
        RegistroHoras.objects.create(
            voluntario=self.voluntario, horas=3, registrado_por_rut="22222222-2"
        )
        RegistroHoras.objects.create(
            voluntario=self.voluntario, horas=2, registrado_por_rut="22222222-2"
        )
        url = f"/api/voluntarios/{self.voluntario.id}/horas/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["horas_acumuladas"], 5)
        self.assertEqual(len(response.data["registros"]), 2)


class AsignacionVoluntarioViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.voluntario = Voluntario.objects.create(
            rut="11111111-1", estado="activo"
        )
        self.asignacion = AsignacionVoluntario.objects.create(
            voluntario=self.voluntario,
            necesidad_id=10,
            estado="asignado",
        )

    def test_listar_asignaciones(self):
        response = self.client.get("/api/asignaciones/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_asignacion(self):
        data = {
            "voluntario": self.voluntario.id,
            "necesidad_id": 20,
            "estado": "propuesto",
        }
        response = self.client.post("/api/asignaciones/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filtrar_por_necesidad_id(self):
        response = self.client.get("/api/asignaciones/", {"necesidad_id": 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_por_estado(self):
        response = self.client.get("/api/asignaciones/", {"estado": "asignado"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filtrar_por_rut_voluntario(self):
        response = self.client.get("/api/asignaciones/", {"rut": "11111111-1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
