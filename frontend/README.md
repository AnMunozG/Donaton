# Frontend - Donatón

SPA (Single Page Application) desarrollada con React 19 + Vite 8, que consume la API del BFF para interactuar con todos los microservicios de la plataforma Donatón.

## Descripción

El frontend es la interfaz de usuario de la plataforma. Permite a los donantes realizar donaciones, a los ciudadanos reportar necesidades, a los encargados gestionar sus centros de acopio y a los voluntarios registrarse y administrar sus horas. Se comunica exclusivamente con el BFF (API Gateway).

## Tecnologías

- React 19
- Vite 8
- Bootstrap 5
- Recharts (gráficos)
- React Router
- Axios (cliente HTTP)
- Tiptap (editor de texto enriquecido)
- Vitest (testing)

## Estructura

```text
frontend/
├── src/
│   ├── api.js                  # Fachada de API con fallback localStorage
│   ├── main.jsx                # Punto de entrada con React Router
│   ├── componentes/
│   │   ├── AuthContext.jsx     # Contexto: user, login, logout, isAuth
│   │   ├── ProtectedRoute.jsx  # Redirige a /login si no autenticado
│   │   ├── RichTextEditor.jsx  # Editor Tiptap
│   │   └── Validaciones.js     # Validaciones de formulario
│   ├── paginas/
│   │   ├── Donacion.jsx        # Formulario de donación pública
│   │   ├── Necesidades.jsx     # Formulario de necesidad ciudadana
│   │   ├── Centros.jsx         # Lista + mapa de centros
│   │   ├── BackOffice.jsx      # Admin panel (dashboard, CRUD)
│   │   ├── Perfil.jsx          # Perfil del usuario logueado
│   │   ├── Login.jsx           # Inicio de sesión
│   │   ├── Registro.jsx        # Registro de usuario
│   │   └── ...
│   ├── servicios/
│   │   ├── api.js              # Instancia Axios con interceptors
│   │   ├── donaciones.js       # Cliente HTTP para donaciones
│   │   ├── centros.js          # Cliente HTTP para centros
│   │   └── necesidades.js      # Cliente HTTP para necesidades
│   └── test/                   # Tests unitarios (Vitest)
├── nginx/                      # Configuración Nginx para producción
├── Dockerfile
├── vite.config.js
├── package.json
└── README.md
```

## Variables de entorno

Crea un archivo `.env` en la raíz de `frontend/`:

| Variable | Descripción | Default |
|----------|-------------|---------|
| `VITE_API_URL` | URL base del BFF | `http://localhost:8080/api` |
| `VITE_GOOGLE_MAPS_API_KEY` | API Key de Google Maps | (requerido para mapa de centros) |

## Requisitos

- Node.js 18 o superior
- npm o yarn

## Instalación

```bash
cd frontend
npm install
```

## Desarrollo

```bash
npm run dev      # http://localhost:5173
```

El frontend en modo desarrollo se comunica con el BFF en `http://localhost:8080/api` (configurado en `vite.config.js` con proxy).

## Producción

```bash
npm run build    # Build de producción en dist/
npm run preview  # Preview del build local
```

En Docker, el frontend se sirve con Nginx en el puerto 80.

## Pruebas Unitarias

```bash
npm run test     # Ejecuta tests con Vitest
```

## Arquitectura de componentes

- **AuthContext**: Gestiona el estado de autenticación del usuario (login, logout, token JWT, datos del perfil).
- **ProtectedRoute**: Componente wrapper que redirige a `/login` si el usuario no está autenticado. Soporta `requiredRole` para rutas de admin/encargado.
- **api.js**: Fachada centralizada que consolida todas las llamadas a la API. Usa localStorage como fallback si el BFF no está disponible.
- **BackOffice.jsx**: Panel de administración con pestañas para gestión de donaciones, necesidades, centros, voluntarios y estadísticas.
