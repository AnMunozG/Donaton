# Backend Necesidades - Donatón

API REST para la gestión de necesidades desarrollada con Django y Django REST Framework. Permite crear, consultar, actualizar y eliminar necesidades de centros de acopio, además de registrar donaciones que impactan en el progreso de cada necesidad.

## Descripción

Este microservicio administra las necesidades de los centros de acopio. Cada necesidad tiene una cantidad requerida, una cantidad recibida y un estado que se actualiza automáticamente cuando se registran donaciones. Soporta necesidades regulares (de centros) y necesidades ciudadanas (reportadas por usuarios).

## Tecnologías

- Python 3
- Django
- Django REST Framework
- Django REST Framework SimpleJWT
- django-cors-headers
- MySQL

## Estructura

```text
necesidades/
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
└── api_necesidades/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── tests.py
```

## Modelos principales

- `EstadoNecesidad`: estados posibles (Pendiente, Activa, Cubierta).
- `Necesidad`: centro_acopio_id, titulo, descripcion, categoria (ALIMENTOS, ROPA, DINERO, SALUD, UTILES, VOLUNTARIADO, OTROS), estado (FK), urgencia (ALTA, MEDIA, BAJA), cantidad_requerida, cantidad_recibida, unidad_medida, solicitante_nombre, solicitante_contacto, detalles (JSON), fecha_creacion, fecha_actualizacion. Incluye propiedad `porcentaje_cubierto`.

## Requisitos

- Python 3.10 o superior
- MySQL en ejecución
- pip y un entorno virtual

## Instalación

1. Clonar el repositorio.
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Donaton/necesidades
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
    - Por defecto apunta a MySQL con la base `necesidades_db`.

5. Ejecutar migraciones.
    ```bash
    python manage.py migrate
    ```

6. Cargar datos de ejemplo si los necesitas.
    ```bash
    python manage.py seed
    ```

## Ejecución

```bash
python manage.py runserver 8003
```

La aplicación quedará disponible en `http://127.0.0.1:8003/`.

## Rutas disponibles

### API REST

Las rutas principales están expuestas bajo `/api/`:

- `/api/necesidades/` — CRUD de necesidades.
- `/api/necesidades/{id}/` — Detalle de una necesidad.
- `/api/necesidades/{id}/registrar-donacion/` — Registrar una donación que impacta en la necesidad (aumenta cantidad_recibida, actualiza estado automáticamente).

### Filtros disponibles

- `GET /api/necesidades/?centro_id=1` — Filtrar por centro de acopio.
- `GET /api/necesidades/?categoria=ALIMENTOS` — Filtrar por categoría.
- `GET /api/necesidades/?estado=Pendiente` — Filtrar por estado.
- `GET /api/necesidades/?urgencia=ALTA` — Filtrar por urgencia.

## Lógica de negocio

### Registrar donación (`registrar_donacion`)

Al registrar una donación sobre una necesidad:
1. Se suma la cantidad donada a `cantidad_recibida`.
2. Si `cantidad_recibida >= cantidad_requerida`, el estado cambia a "Cubierta".
3. Si `cantidad_recibida > 0` y el estado era "Pendiente", cambia a "Activa".

## Autenticación

- La autenticación se realiza mediante JWT (SimpleJWT).
- Los endpoints de lectura y registro de donación son públicos (accesibles desde el BFF).
- Las operaciones de escritura para necesidades regulares requieren token JWT con rol admin o encargado.

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
