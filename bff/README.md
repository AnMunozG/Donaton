# BFF (Backend-for-Frontend) - Donatón

API Gateway que sirve como punto de entrada único para el frontend. Desarrollado con Django y Django Ninja, orquesta las llamadas a los microservicios y maneja autenticación, perfiles y rutas de negocio simplificadas.

## Descripción

El BFF (Backend-for-Frontend) actúa como intermediario entre el frontend React y los microservicios. Centraliza la autenticación (login, registro, perfil), provee endpoints simplificados para el frontend y gestiona tokens JWT de sistema para comunicarse con los microservicios.

## Tecnologías

- Python 3
- Django
- Django Ninja (API framework async)
- JWT (PyJWT)
- httpx (cliente HTTP async)
- Redis (opcional: circuit breaker, caché)

## Estructura

```text
bff/
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
└── gateway/
    ├── api.py              # Definición de endpoints NinjaAPI
    ├── clients/            # Clientes HTTP para microservicios
    │   ├── usuarios_client.py
    │   ├── logistica_client.py
    │   ├── donaciones_client.py
    │   ├── necesidades_client.py
    │   └── voluntarios_client.py
    ├── services/           # Lógica de negocio del BFF
    │   ├── auth_service.py
    │   ├── centro_service.py
    │   ├── donacion_service.py
    │   ├── necesidad_service.py
    │   ├── voluntario_service.py
    │   └── static_service.py
    ├── schemas/            # Esquemas de validación Ninja
    └── tests/
        ├── conftest.py
        └── test_donaciones.py
```

## Requisitos

- Python 3.10 o superior
- Microservicios corriendo (usuarios, logistica, donaciones, necesidades, voluntarios)

## Instalación

1. Clonar el repositorio.
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Donaton/bff
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

4. Ejecutar migraciones (solo para internals de Django).
    ```bash
    python manage.py migrate
    ```

## Ejecución

```bash
python manage.py runserver 8080
```

La API quedará disponible en `http://127.0.0.1:8080/api/`.

## Endpoints

### Autenticación

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/api/auth/login` | - | Iniciar sesión (retorna JWT del BFF) |
| POST | `/api/auth/register` | - | Registrar nuevo usuario |
| GET | `/api/auth/me` | JWT | Obtener perfil del usuario autenticado |
| PUT | `/api/auth/profile` | JWT | Actualizar perfil |
| GET | `/api/auth/usuarios` | Admin | Listar todos los usuarios |
| PATCH | `/api/auth/usuarios/{rut}` | Admin | Actualizar usuario (admin) |

### Centros

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/centros` | - | Listar centros de acopio |
| GET | `/api/centros/{id}` | - | Detalle de centro |
| POST | `/api/centros` | Admin | Crear centro |
| PUT | `/api/centros/{id}` | Encargado/Admin | Actualizar centro |
| GET | `/api/centros/{id}/stats` | - | Estadísticas del centro |
| GET | `/api/centros/{id}/inventario` | - | Inventario del centro |

### Donaciones

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/donaciones` | - | Listar donaciones (filtros: estado, centro_code, tipo, origen) |
| POST | `/api/donaciones` | - | Crear donación individual |
| POST | `/api/donaciones/multi` | - | Crear donación con múltiples items |
| GET | `/api/donaciones/{id}` | - | Detalle de donación |
| PATCH | `/api/donaciones/{id}/estado` | Encargado/Admin | Actualizar estado |
| DELETE | `/api/donaciones/{id}` | Admin | Eliminar donación |
| GET | `/api/donaciones/stats/resumen` | - | Estadísticas de donaciones |

### Necesidades

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/necesidades` | - | Listar necesidades (filtros: estado, centro_code, urgencia) |
| POST | `/api/necesidades` | Encargado/Admin | Crear necesidad |
| GET | `/api/necesidades/{id}` | - | Detalle de necesidad |
| PUT | `/api/necesidades/{id}` | Encargado/Admin | Actualizar necesidad |
| POST | `/api/necesidades/{id}/activar` | Encargado/Admin | Activar necesidad (asigna urgencia) |
| GET | `/api/necesidades/ciudadanas` | - | Listar necesidades ciudadanas |
| POST | `/api/necesidades/ciudadanas` | - | Crear necesidad ciudadana |
| PATCH | `/api/necesidades/ciudadanas/{id}` | - | Actualizar necesidad ciudadana |
| DELETE | `/api/necesidades/ciudadanas/{id}` | - | Eliminar necesidad ciudadana |
| GET | `/api/necesidades/{id}/propuestas` | - | Listar propuestas |
| POST | `/api/propuestas` | JWT | Crear propuesta |

### Voluntarios

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/voluntarios` | - | Listar voluntarios (filtros: estado, centro, habilidad, disponibilidad) |
| GET | `/api/voluntarios/mi-perfil` | JWT | Perfil de voluntario del usuario |
| POST | `/api/voluntarios` | JWT | Registrarse como voluntario |
| GET | `/api/voluntarios/{id}` | JWT | Detalle de voluntario |
| PUT | `/api/voluntarios/{id}` | JWT | Actualizar datos de voluntario |
| PATCH | `/api/voluntarios/{id}/estado` | Encargado/Admin | Cambiar estado de voluntario |
| DELETE | `/api/voluntarios/{id}` | Admin | Eliminar voluntario |
| POST | `/api/voluntarios/{id}/horas` | JWT | Registrar horas trabajadas |
| GET | `/api/voluntarios/{id}/horas` | JWT | Listar horas registradas |

### Otros

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/health` | - | Estado de todos los servicios |
| GET | `/api/static/*` | - | Catálogos y contenido estático |
| POST | `/api/auth/agradecimientos` | Encargado/Admin | Crear agradecimiento |
| GET | `/api/auth/agradecimientos/recibidos` | JWT | Ver agradecimientos recibidos |
| POST | `/api/auth/centros/seguir` | JWT | Seguir un centro |
| DELETE | `/api/auth/centros/{id}/seguir` | JWT | Dejar de seguir un centro |
| GET | `/api/auth/logros` | JWT | Listar logros disponibles |
| POST | `/api/auth/logros/verificar` | JWT | Verificar y otorgar logros |
| GET | `/api/auth/impacto` | JWT | Ver impacto personal |
| GET | `/api/auth/certificado/{year}` | JWT | Descargar certificado anual PDF |

## Autenticación

El BFF usa JWT con tres niveles de permiso:
- **AuthBearer**: cualquier token JWT válido.
- **AdminBearer**: token JWT con `rol == "admin"`.
- **EncargadoOrAdminBearer**: token JWT con `rol` igual a `"admin"` o `"encargado"`.

El payload del JWT contiene: `rut`, `nombre`, `email`, `rol`, `centro_acopio_id`, `uat` (token de Usuarios), `uat_refresh`.

## Pruebas

```bash
pytest
```

## Configuración

La configuración principal está en `config/settings.py`.

| Variable | Descripción | Default |
|----------|-------------|---------|
| `JWT_SECRET` | Secreto para firmar tokens del BFF | `BFF_JWT_SECRET` o `SECRET_KEY` |
| `USUARIOS_URL` | URL del microservicio de Usuarios | `http://localhost:8002` |
| `LOGISTICA_URL` | URL del microservicio de Logística | `http://localhost:8001` |
| `DONACIONES_URL` | URL del microservicio de Donaciones | `http://localhost:8003` |
| `NECESIDADES_URL` | URL del microservicio de Necesidades | `http://localhost:8004` |
| `VOLUNTARIOS_URL` | URL del microservicio de Voluntarios | `http://localhost:8005` |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS | `http://localhost:5173,http://localhost:80` |
