Microservicio de Gestion de Usuarios
Este proyecto consiste en un microservicio de backend desarrollado con Django 5 y Django Rest Framework, diseñado para la administracion y autenticacion de usuarios mediante JSON Web Tokens (JWT). El sistema esta configurado para integrarse con motores de base de datos MySQL/MariaDB.

Stack Tecnologico
Lenguaje: Python 3.11+

Framework Base: Django 5.0

API Framework: Django Rest Framework (DRF)

Autenticacion: SimpleJWT (OAuth2 compatible)

Base de Datos: MariaDB (vía XAMPP o nativo)

Documentacion: drf-spectacular (OpenAPI 3.0 / Swagger)

Requisitos Previos
Python 3.11 o superior.

XAMPP con servicio MySQL activo.

Gestor de dependencias pip.

Instalacion y Configuracion
1. Clonar el repositorio e instalar dependencias
git clone 
cd Usuario-Microservicio
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

2. Configuracion de Base de Datos
Es necesario crear una base de datos en su gestor local (phpMyAdmin u otro) con el nombre definido en el archivo settings.py. Por defecto: usuarios_db.

Notas de Compatibilidad (MariaDB)
Debido a las restricciones de version en entornos locales como XAMPP, el archivo config/init.py incluye parches de compatibilidad para versiones de MariaDB anteriores a la 10.5:

Sustituye el driver por defecto por PyMySQL.

Deshabilita la validacion estricta de la version del motor.

Desactiva la clausula RETURNING en las sentencias SQL para asegurar compatibilidad con versiones Legacy.

Despliegue en Desarrollo
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Documentacion de la API
Una vez iniciado el servidor, las interfaces estan disponibles en:

Swagger UI: http://127.0.0.1:8000/api/docs/

Redoc: http://127.0.0.1:8000/api/redoc/

Seguridad
La API implementa autenticacion por cabeceras Authorization: Bearer . Los endpoints protegidos requieren un token de acceso valido generado a partir del login.