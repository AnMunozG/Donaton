# Donatón

Plataforma web de donaciones transparentes que conecta donantes, municipalidades y equipos de logística para la ayuda humanitaria. Arquitectura de microservicios orquestada con Docker Compose.

## Arquitectura

```
┌──────────┐     ┌─────────────────────────────────────┐     ┌───────────────┐
│ Frontend │────▶│              BFF (API Gateway)       │────▶│  Usuarios    │
│ (React)  │     │        Django + Django Ninja         │     │  (Django)    │
│  :80     │     │               :8080                  │     │  :8002       │
└──────────┘     │                                      │     ├──────────────┤
                 │  - Auth (login/register/profile)      │────▶│  Logística   │
                 │  - Centros CRUD + inventario          │     │  (Django)    │
                 │  - Donaciones CRUD + stats            │     │  :8001       │
                 │  - Necesidades CRUD + Stats           │     ├──────────────┤
                 │  - Catálogos / contenido estático     │────▶│  Donaciones  │
                 └─────────────────────────────────────┘        │  (Django)    │
                                                     |          │  :8003       │
                                                     |        ├──────────────┤
                                                     |────▶ │  Necesidades  │
                                                            │  (Django)    │
                                                            │  :8003       │
                                                            └──────────────┘
- **Frontend**: React 19 + Vite + Bootstrap 5 + Recharts
- **BFF** (Backend-for-Frontend): Django 5 + Django Ninja (API Gateway)
- **Usuarios**: Django 5 + DRF + SimpleJWT (gestión de usuarios)
- **Logística**: Django 5 + DRF + SimpleJWT (centros, inventario JSON)
- **Donaciones**: Django 5 + DRF + drf-spectacular (donaciones CRUD + estadísticas)
- **Necesidades**: Django 5 + DRF + drf-spectacular (Necesidades CRUD + estadísticas)


## Requisitos

- Docker y Docker Compose
- Node.js 18+ (para desarrollo del frontend sin Docker)
- Python 3.12+ (para desarrollo de servicios sin Docker)
- Git

## Ejecución con Docker (producción local)

```bash
# Clonar e iniciar todos los servicios
git clone <repo-url>
cd Donaton
docker compose up -d
```

Servicios disponibles:

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost |
| BFF API  | http://localhost:8080/api |
| BFF Admin| http://localhost:8080/admin |
| Usuarios API | http://localhost:8002/api/ |
| Usuarios Docs | http://localhost:8002/api/docs/ |
| Logística API | http://localhost:8001/api/ |
| Logística Docs | http://localhost:8001/api/docs/ |
| Donaciones API | http://localhost:8003/api/ |
| Necesidades Docs | http://localhost:8004/api/docs/ |

## Comandos útiles (Makefile)

```bash
make up        # Iniciar servicios
make down      # Detener servicios
make build     # Reconstruir imágenes
make logs      # Ver logs en tiempo real
make restart   # Reiniciar servicios
make clean     # Detener y eliminar volúmenes (borra datos)
make test SERVICE=bff    # Ejecutar tests de un servicio
make shell SERVICE=bff   # Shell de Django en un servicio
```

## Desarrollo sin Docker

### Frontend

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
npm run test     # Tests unitarios (Vitest)
npm run build    # Build producción
```

### BFF

```bash
cd bff
python -m venv venv
venv\Scripts\activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8080
```

### Usuarios

```bash
cd usuarios
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Requiere MySQL con base 'usuarios_db'
python manage.py migrate
python manage.py seed
python manage.py runserver 8000
```

### Logística

```bash
cd logistica
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Requiere MySQL con base 'backend_logistica'
python manage.py migrate
python manage.py seed
python manage.py runserver 8001
```

### Donaciones

```bash
cd donaciones
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Requiere MySQL con base 'backend_donaciones'
python manage.py migrate
python manage.py runserver 8002
```

## Variables de entorno

Copia el archivo `.env` incluido y ajusta según sea necesario:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `MYSQL_ROOT_PASSWORD` | Contraseña root de MySQL | `admin` |
| `LOGISTICA_JWT_SECRET` | Secreto JWT compartido con logística | (requerido) |
| `BFF_JWT_SECRET` | Secreto JWT del BFF | (auto-generado) |
| `DJANGO_DEBUG` | Modo debug | `True` |

## Estructura del proyecto

```
Donaton/
├── .env                     # Variables de entorno
├── docker-compose.yml       # Orquestación de servicios
├── Makefile                 # Comandos de ayuda
├── README.md
│
├── frontend/                # React SPA
│   ├── src/
│   │   ├── api.js           # Fachada de API con fallback localStorage
│   │   ├── main.jsx         # Punto de entrada con React Router
│   │   ├── componentes/     # Componentes reutilizables
│   │   ├── paginas/         # Páginas de la aplicación
│   │   ├── servicios/       # Clientes HTTP (Axios)
│   │   └── test/            # Tests unitarios
│   ├── nginx/               # Configuración Nginx
│   └── package.json
│
├── bff/                     # Backend-for-Frontend (API Gateway)
│   ├── config/
│   │   ├── settings.py      # Configuración Django
│   │   └── urls.py          # Rutas del BFF
│   ├── gateway/
│   │   ├── api.py           # Definición de endpoints NinjaAPI
│   │   ├── clients/         # Clientes HTTP para microservicios
│   │   ├── services/        # Lógica de negocio del BFF
│   │   ├── schemas/         # Esquemas de validación Ninja
│   │   ├── events.py        # Bus de eventos (Redis pub/sub)
│   │   └── tests/           # Tests del BFF
│   └── requirements.txt
│
├── usuarios/                # Microservicio de Usuarios
│   ├── config/
│   │   └── settings.py      # Django + DRF + SimpleJWT
│   ├── api_servicio/
│   │   ├── models.py        # Usuario con RUT chileno
│   │   ├── views.py         # CRUD + registro
│   │   └── serializers.py
│   └── requirements.txt
│
├── donaciones/              # Microservicio de Donaciones
│   ├── confing/
│   │   └── settings.py      # Django + DRF + MySQL
│   ├── api_donaciones/
│   │   ├── models.py        # Donacion
│   │   ├── views.py         # ViewSet con filtros + stats
│   │   └── serializers.py
│   ├── management/          # Comandos seed
│   └── requirements.txt
│
└── logistica/               # Microservicio de Logística
|   ├── config/
|   │   └── settings.py      # Django + DRF + SimpleJWT
|   ├── logistica/
|   │   ├── models.py        # CentroAcopio con inventario JSON
|   │   ├── views.py         # ViewSets con permisos
|   │   └── serializers.py
|   └── requirements.txt
└── Necesidades/               # Microservicio de Necesidades
    ├── config/
    │   └── settings.py      # Django + DRF + SimpleJWT
    ├── logistica/
    │   ├── models.py        # JSON de necesidades
    │   ├── views.py         # ViewSets
    │   └── serializers.py
    └── requirements.txt
```

## Endpoints de la API (BFF)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/api/health` | - | Estado de los servicios |
| POST | `/api/auth/login` | - | Iniciar sesión |
| POST | `/api/auth/register` | - | Registrar usuario |
| GET | `/api/auth/me` | JWT | Perfil del usuario |
| PUT | `/api/auth/profile` | JWT | Actualizar perfil |
| GET | `/api/centros` | - | Listar centros |
| GET | `/api/centros/{id}` | - | Detalle de centro |
| POST | `/api/centros` | Admin | Crear centro |
| PUT | `/api/centros/{id}` | JWT | Actualizar centro |
| GET | `/api/centros/{id}/stats` | - | Estadísticas de centro |
| GET | `/api/centros/{id}/inventario` | - | Inventario de centro |
| GET | `/api/donaciones` | - | Listar donaciones (filtros: estado, centro_code, tipo) |
| GET | `/api/donaciones/{code}` | - | Detalle de donación |
| POST | `/api/donaciones` | JWT | Crear donación (actualiza inventario en logística) |
| PATCH | `/api/donaciones/{code}/estado` | JWT | Actualizar estado |
| GET | `/api/donaciones/stats/resumen` | - | Estadísticas de donaciones |
| GET | `/api/necesidades` | - | Listar necesidades |
| POST | `/api/necesidades` | JWT | Crear necesidad |
| GET | `/api/static/*` | - | Catálogos y contenido estático |
