# Backend Donaciones - Donatón

API REST para la gestión de donaciones desarrollada con Django y Django REST Framework. El servicio administra registros de donaciones, su estado y estadísticas básicas, con documentación automática de la API y autenticación basada en JWT cuando se integra con el resto de la plataforma.

## Descripción

Este microservicio centraliza la administración de donaciones dentro de la solución Donatón. Permite crear, consultar, actualizar y eliminar donaciones, además de exponer un resumen estadístico y datos listos para ser consumidos por el BFF.

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
Donaciones/
├── manage.py
├── requirements.txt
├── Dockerfile
├── entrypoint.sh
└── api_donaciones/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── admin.py
    ├── tests.py
    └── management/
        └── commands/
```

## Modelo principal

- `Donacion`: tipo, cantidad, unidad, origen, centroId, fecha, estado, detalles, created_at y updated_at.

## Requisitos

- Python 3.10 o superior
- MySQL en ejecución
- pip y un entorno virtual

## Instalación

1. Clonar el repositorio.
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Donaton/donaciones
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

4. Revisar la configuración de base de datos en `confing/settings.py`.
    - Por defecto apunta a MySQL con la base `backend_donaciones`.
    - Ajusta usuario, contraseña, host y puerto según tu entorno.

5. Ejecutar migraciones.
    ```bash
    python manage.py migrate
    ```

6. Cargar datos de ejemplo si los necesitas.
    ```bash
    python manage.py seed
    ```

## Ejecución

Inicia el servidor de desarrollo con:

```bash
python manage.py runserver 8002
```

La aplicación quedará disponible en `http://127.0.0.1:8002/`.

## Rutas disponibles

### Administración y documentación

- `/admin/` - Panel de administración de Django.
- `/api/schema/` - Esquema OpenAPI.
- `/api/docs/` - Swagger UI.

### API REST

Las rutas principales están expuestas bajo `/api/`:

- `/api/donaciones/` - CRUD de donaciones.
- `/api/donaciones/{id}/` - Detalle de una donación.
- `/api/donaciones/stats/` - Estadísticas agregadas.

## Autenticación y permisos

- El microservicio está preparado para integrarse con JWT dentro del ecosistema Donatón.
- El BFF consume este servicio para crear, listar, filtrar y actualizar donaciones.

## API y serialización

- `DonacionSerializer` expone el identificador como `id` a partir de `idDonacion`.
- El endpoint de estadísticas calcula totales, distribución por estado y por tipo.

## Pruebas

Ejecuta la suite de pruebas con:

```bash
python manage.py test
```

## Migraciones

Si modificas modelos en `api_donaciones/models.py`, crea y aplica migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Configuración importante

La configuración principal está en `confing/settings.py`.

- `DEBUG` controla el modo de depuración.
- `DATABASES` define la conexión a MySQL.
- `REST_FRAMEWORK` activa la configuración base de la API.
- `SPECTACULAR_SETTINGS` define el título y la descripción de la documentación.

## Notas

- Mantén las credenciales fuera del control de versiones cuando pases a entornos reales.
- Si vas a consumir la API desde el frontend o desde el BFF, revisa también la configuración de CORS.

## Autoría

- AnMunozG
    - GitHub: @AnMunozG
- yasser-duoc
    - GitHub: @yasser-duoc
- MartinIgnaci0
    - GitHub: @MartinIgnaci0
