# Backend Usuarios - Donatón

API REST para la gestión de usuarios desarrollada con Django y Django REST Framework. Administra registro, autenticación y perfiles de usuarios del ecosistema Donatón, con autenticación JWT y validación de RUT chileno.

## Descripción

Este microservicio centraliza la administración de usuarios. Permite registrar nuevos usuarios con validación de RUT chileno (módulo 11), autenticarse mediante JWT, gestionar perfiles y administrar logros de gamificación.

## Tecnologías

- Python 3
- Django
- Django REST Framework
- Django REST Framework SimpleJWT
- django-cors-headers
- MySQL

## Estructura

```text
usuarios/
├── manage.py
├── requirements.txt
├── Dockerfile
├── entrypoint.sh
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api_servicio/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── tests.py
    └── migrations/
```

## Modelos principales

- `Usuario` (AbstractUser): rut (PK, validación módulo 11), USERNAME_FIELD = 'rut'. Hereda username, email, first_name, last_name, is_staff, is_active, date_joined. Campo adicional: centro_acopio_id (para rol encargado).
- `Logro`: codigo (slug único), nombre, descripcion, icono, categoria, orden.
- `LogroUsuario`: usuario (FK), logro (FK), fecha_obtenido, progreso. unique_together en (usuario, logro).

## Requisitos

- Python 3.10 o superior
- MySQL en ejecución
- pip y un entorno virtual

## Instalación

1. Clonar el repositorio.
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Donaton/usuarios
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
    - Por defecto apunta a MySQL con la base `usuarios_db`.

5. Ejecutar migraciones.
    ```bash
    python manage.py migrate
    ```

6. Cargar datos de ejemplo.
    ```bash
    python manage.py seed
    ```

## Ejecución

```bash
python manage.py runserver 8000
```

La aplicación quedará disponible en `http://127.0.0.1:8000/`.

## Rutas disponibles

### Autenticación

- `POST /api/login/` — Iniciar sesión (retorna access + refresh tokens).
- `POST /api/token/refresh/` — Refrescar token de acceso.

### Usuarios

- `GET/POST /api/usuarios/` — Listar usuarios (autenticado) / Registrar usuario (público).
- `GET/PUT/PATCH/DELETE /api/usuarios/{id}/` — CRUD de usuario.

### Logros

- `GET/POST /api/logros/` — Listar logros (público) / Crear logro (admin).
- `GET /api/mis-logros/` — Logros del usuario autenticado.
- `POST /api/mis-logros/verificar/` — Verificar y otorgar logros según estadísticas.

## Autenticación

- La autenticación se realiza mediante JWT (SimpleJWT).
- El registro es público (`AllowAny`).
- El listado de usuarios requiere autenticación.
- Los logros de lectura son públicos; escritura requiere admin.

## Validación de RUT

El campo `rut` del modelo Usuario valida automáticamente:
- Formato: 7 u 8 dígitos + guión + dígito verificador (0-9 o K).
- Cálculo del dígito verificador usando Módulo 11.

## Pruebas

Ejecuta la suite de pruebas con:

```bash
python manage.py test
```

## Configuración importante

La configuración principal está en `config/settings.py`.

- `DEBUG` controla el modo de depuración.
- `DATABASES` define la conexión a MySQL.
- `AUTH_USER_MODEL` apunta a `api_servicio.Usuario`.
- `SIMPLE_JWT` configura la vida útil de los tokens (24h access, 7d refresh).
- `REST_FRAMEWORK` activa JWT como autenticación por defecto.
