# Backend Voluntarios - Donatón

API REST para la gestión de voluntarios desarrollada con Django y Django REST Framework. Permite registrar voluntarios, gestionar horas trabajadas y asignaciones a necesidades del microservicio de Necesidades.

## Descripción

Este microservicio administra el registro de voluntarios que desean ayudar en los centros de acopio. Permite crear, consultar, actualizar y eliminar voluntarios, además de registrar horas de trabajo y asignar voluntarios a necesidades específicas.

## Tecnologías

- Python 3
- Django
- Django REST Framework
- Django REST Framework SimpleJWT
- django-cors-headers
- MySQL

## Estructura

```text
voluntarios/
├── manage.py
├── requirements.txt
├── Dockerfile
├── entrypoint.sh
├── pytest.ini
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api_voluntarios/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── tests.py
```

## Modelos principales

- `Voluntario`: rut, disponibilidad (diaria/semanal/fines_semana/emergencia), habilidades (JSON), centro_preferido, estado (pendiente/activo/inactivo), fecha_registro. Calcula horas_acumuladas y estado activo.
- `RegistroHoras`: voluntario (FK), horas, descripcion, registrado_por_rut, fecha.
- `AsignacionVoluntario`: voluntario (FK), necesidad_id (enlace lógico a Necesidades), estado (propuesto/asignado/completado/cancelado). Constraint unique_together en (voluntario, necesidad_id).

## Requisitos

- Python 3.10 o superior
- MySQL en ejecución
- pip y un entorno virtual

## Instalación

1. Clonar el repositorio.
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Donaton/voluntarios
    ```

2. Crear y activar un entorno virtual.
    ```bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    source venv/bin/activate  # Linux / macOS
    ```

3. Instalar dependencias.
    ```bash
    pip install -r requirements.txt
    ```

4. Revisar la configuración de base de datos en `config/settings.py`.
    - Por defecto apunta a MySQL con la base `voluntarios_db`.

5. Ejecutar migraciones.
    ```bash
    python manage.py migrate
    ```

## Ejecución

```bash
python manage.py runserver 8005
```

La aplicación quedará disponible en `http://127.0.0.1:8005/`.

## Rutas disponibles

### API REST

Las rutas principales están expuestas bajo `/api/`:

- `/api/voluntarios/` — CRUD de voluntarios.
- `/api/voluntarios/{id}/` — Detalle de un voluntario.
- `/api/voluntarios/{id}/registrar-horas/` — Registrar horas trabajadas.
- `/api/voluntarios/{id}/horas/` — Listar horas registradas.
- `/api/asignaciones/` — CRUD de asignaciones de voluntarios a necesidades.

### Filtros disponibles

- `GET /api/voluntarios/?estado=activo` — Filtrar por estado.
- `GET /api/voluntarios/?activo=true` — Filtrar por actividad.
- `GET /api/voluntarios/?centro_preferido=1` — Filtrar por centro.
- `GET /api/voluntarios/?disponibilidad=diaria` — Filtrar por disponibilidad.
- `GET /api/voluntarios/?habilidad=enfermeria` — Filtrar por habilidad.
- `GET /api/voluntarios/?rut=11111111-1` — Filtrar por RUT.

### Filtros de asignaciones

- `GET /api/asignaciones/?rut=11111111-1` — Filtrar por RUT de voluntario.
- `GET /api/asignaciones/?necesidad_id=10` — Filtrar por necesidad.
- `GET /api/asignaciones/?estado=asignado` — Filtrar por estado.

## Autenticación

- La autenticación se realiza mediante JWT (SimpleJWT).
- Los endpoints de lectura (listar voluntarios) son públicos.
- Las operaciones de escritura requieren token JWT válido.
- Cambiar estado y eliminar requieren rol admin o encargado.

## Pruebas

Ejecuta la suite de pruebas con:

```bash
python manage.py test
# o con pytest
pytest
```

## Configuración importante

La configuración principal está en `config/settings.py`.

- `DEBUG` controla el modo de depuración.
- `DATABASES` define la conexión a MySQL.
- `REST_FRAMEWORK` activa JWT como autenticación por defecto.
- `SIMPLE_JWT` configura la vida útil de los tokens.
