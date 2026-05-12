# Backend Logística - Fullstack 3

Sistema backend para gestión de logística desarrollado con Django REST Framework.

## 📋 Descripción

Este proyecto es un backend de logística que proporciona una API REST completa para la gestión de operaciones logísticas. Utiliza Django como framework principal y Django REST Framework para la creación de APIs.

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Django** - Framework web
- **Django REST Framework** - Para la creación de APIs REST
- **SQLite** - Base de datos (desarrollo)
- **pip** - Gestor de dependencias de Python

## 📁 Estructura del Proyecto

```
backend_logistica/
├── db.sqlite3                 # Base de datos SQLite
├── manage.py                  # Utilidad de línea de comandos de Django
├── backend_logistica/         # Configuración principal del proyecto
│   ├── __init__.py
│   ├── asgi.py               # ASGI config
│   ├── settings.py           # Configuración del proyecto
│   ├── urls.py               # URLs principales
│   └── wsgi.py               # WSGI config
└── logistica/                # Aplicación principal
    ├── __init__.py
    ├── admin.py              # Configuración del admin
    ├── apps.py               # Configuración de la app
    ├── models.py             # Modelos de datos
    ├── serializers.py        # Serializadores DRF
    ├── tests.py              # Pruebas unitarias
    ├── urls.py               # URLs de la app
    ├── views.py              # Vistas de la API
    └── migrations/           # Migraciones de base de datos
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.x instalado
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd BackendLogistica_Fullstack3
   ```

2. **Ejecutar un entorno virtual**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar migraciones**
   ```bash
   python manage.py migrate
   ```

5. **Crear un superusuario** (opcional, para acceder al admin)
   ```bash
   python manage.py createsuperuser
   ```

## 🏃 Ejecutar el Proyecto

Para iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

### Acceso al Admin de Django

Si creó un superusuario, puede acceder al admin en:
```
http://127.0.0.1:8000/admin/
```

## 📚 API Endpoints

Los endpoints principales se encuentran en la aplicación `logistica`. Consulte `logistica/urls.py` para ver las rutas disponibles.

### Ejemplo de URLs

```python
# En logistica/urls.py
urlpatterns = [
    # Agregar endpoints aquí
]
```

## 🗄️ Base de Datos

Este proyecto utiliza SQLite por defecto para desarrollo. Para producción.

### Crear una nueva migración

Después de modificar modelos en `logistica/models.py`:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Pruebas

Ejecute las pruebas unitarias con:

```bash
python manage.py test
```

## ⚙️ Configuración

La configuración principal se encuentra en `backend_logistica/settings.py`. Algunas variables importantes:

- `DEBUG` - Modo de depuración
- `ALLOWED_HOSTS` - Hosts permitidos
- `INSTALLED_APPS` - Aplicaciones instaladas
- `DATABASES` - Configuración de base de datos

## 📝 Notas de Desarrollo

- Asegúrarse de crear un entorno virtual antes de instalar dependencias
- No incluir archivos sensibles (contraseñas, claves API) en el control de versiones

## 📄 Licencia

[Especificar la licencia del proyecto]

## 👤 Autor
- AnMunozG
    - GitHub: @AnMunozG
- yasser-duoc
    - GitHub: @yasser-duoc
- MartinIgnaci0
    - GitHub: MartinIgnaci0

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
