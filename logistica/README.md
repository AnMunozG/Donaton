# Backend Logística - Fullstack 3

API REST para gestión logística desarrollada con Django y Django REST Framework. El proyecto modela centros de acopio, productos e inventario, con documentación automática de la API y autenticación basada en JWT.

## Descripción

Este backend centraliza la administración de una solución logística orientada a ayuda humanitaria. Permite crear y consultar centros de acopio, administrar productos y registrar inventario entre ambos modelos.

## Tecnologías

- Python 3
- Django
- Django REST Framework
- Django REST Framework SimpleJWT
- drf-spectacular para OpenAPI y Swagger
- django-cors-headers
- MySQL

## Estructura

```text
BackendLogistica_Fullstack3/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── logistica/
     ├── models.py
     ├── serializers.py
     ├── views.py
     ├── urls.py
     ├── admin.py
     ├── tests.py
     └── migrations/
```

## Modelos principales

- `CentroAcopio`: nombre, dirección, capacidad total, capacidad usada y coordenadas.
- `Producto`: nombre, categoría, descripción, unidad de medida, fecha de creación y estado activo.
- `Inventario`: relación entre producto y centro de acopio con cantidad y fecha de actualización.

## Requisitos

- Python 3.10 o superior
- MySQL en ejecución
- pip y un entorno virtual

## Instalación

1. Clonar el repositorio.
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd BackendLogistica_Fullstack3
    ```

2. Crear y activar un entorno virtual.
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux / macOS
    source venv/bin/activate
    ```

3. Instalar dependencias.
    ```bash
    pip install -r requirements.txt
    ```

4. Revisar la configuración de base de datos en `config/settings.py`.
    - Por defecto apunta a MySQL con la base `backend_logistica_db`.
    - Ajusta usuario, contraseña, host y puerto según tu entorno.

5. Ejecutar migraciones.
    ```bash
    python manage.py migrate
    ```

6. Crear un superusuario si vas a usar el admin.
    ```bash
    python manage.py createsuperuser
    ```

## Ejecución

Inicia el servidor de desarrollo con:

```bash
python manage.py runserver 8001
```

La aplicación quedará disponible en `http://127.0.0.1:8001/`.

## Rutas disponibles

### Administración y documentación

- `/admin/` - Panel de administración de Django.
- `/api/schema/` - Esquema OpenAPI.
- `/api/docs/` - Swagger UI.

### API REST

Las rutas principales están expuestas bajo `/api/`:

- `/api/productos/` - CRUD de productos.
- `/api/centros/` - CRUD de centros de acopio.
- `/api/inventario/` - CRUD de inventario.

## Autenticación y permisos

- `ProductoViewSet` requiere usuario administrador.
- `CentroAcopioViewSet` e `InventarioViewSet` requieren usuario autenticado.
- La autenticación configurada en el proyecto usa JWT.

## API y serialización

- La documentación automática se genera con drf-spectacular.
- `Inventario` expone campos calculados como `productoNombre` y `centroNombre` para facilitar el consumo desde frontend.

## Pruebas

Ejecuta la suite de pruebas con:

```bash
python manage.py test
```

## Migraciones

Si modificas modelos en `logistica/models.py`, crea y aplica migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Configuración importante

La configuración principal está en `config/settings.py`.

- `DEBUG` controla el modo de depuración.
- `DATABASES` define la conexión a MySQL.
- `REST_FRAMEWORK` activa JWT como autenticación por defecto.
- `SPECTACULAR_SETTINGS` define el título y la descripción de la documentación.

## Notas

- Mantén las credenciales fuera del control de versiones cuando pases a entornos reales.
- Si vas a consumir la API desde un frontend, revisa también la configuración de CORS.

## Autoría

- AnMunozG
    - GitHub: @AnMunozG
- yasser-duoc
    - GitHub: @yasser-duoc
- MartinIgnaci0
    - GitHub: @MartinIgnaci0
