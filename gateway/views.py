from ninja import NinjaAPI, Schema  # Importamos Schema
import httpx
from django.conf import settings

# Instanciamos la API de Ninja
api = NinjaAPI(title="BFF Gateway Asíncrono")

# --- DEFINICIÓN DE DATOS (SCHEMAS) ---
class LoginPayload(Schema):
    rut: str
    password: str

# --- ENDPOINTS ---

@api.post("/auth/login")
async def login_proxy(request, data: LoginPayload):  # <-- Ahora usamos el Schema
    """
    Recibe credenciales (RUT y Password) y las manda al micro de usuarios.
    """
    url = f"{settings.MICROSERVICIOS['USUARIOS']}login/"
    
    async with httpx.AsyncClient() as client:
        try:
            # Enviamos data.dict() que convierte el Schema a un diccionario normal
            response = await client.post(url, json=data.dict(), timeout=5.0)
            
            # Devolvemos la respuesta del micro al frontend
            return response.json()
        except httpx.ConnectError:
            return {"error": "El microservicio de Usuarios no está disponible"}, 503
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

@api.get("/dashboard")
async def get_dashboard_data(request):
    """
    Junta datos de Usuarios y Productos en una sola respuesta asíncrona.
    """
    token = request.headers.get('Authorization')
    headers = {'Authorization': token} if token else {}

    async with httpx.AsyncClient() as client:
        try:
            # Lanzamos ambas peticiones
            res_usuario = await client.get(
                f"{settings.MICROSERVICIOS['USUARIOS']}usuarios/me/", 
                headers=headers
            )
            
            res_productos = await client.get(
                f"{settings.MICROSERVICIOS['PRODUCTOS']}productos/", 
                headers=headers
            )

            return {
                "usuario": res_usuario.json() if res_usuario.status_code == 200 else "Error en servicio usuarios",
                "productos": res_productos.json() if res_productos.status_code == 200 else "Error en servicio productos",
                "bff_status": "consolidado_asincrono"
            }
        except Exception as e:
            return {"error": f"Error de conexión: {str(e)}"}, 500