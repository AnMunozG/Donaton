from ninja import NinjaAPI
from ninja.security import HttpBearer
from ninja.errors import ValidationError as NinjaValidationError
import jwt
from django.conf import settings
from typing import Optional

from .exceptions import BffError
from .schemas.auth import LoginIn, LoginOut, RegisterIn, UserOut, UserUpdateIn
from .schemas.centros import CentroCreate, CentroUpdate, CentroOut, CentroStatsOut, InventarioItem, RutaRequest, RutaOut
from .schemas.donaciones import DonacionCreate, DonacionUpdate, DonacionOut, DonacionStatsOut
from .schemas.necesidades import NecesidadCreate, NecesidadUpdate, NecesidadOut, PropuestaCreate, PropuestaOut
from .schemas.static import (TipoRecursoOut, UnidadOut, EquipoOut, GobernanzaOut, HitoOut, ValorOut, ReporteOut, HealthOut,
                             RegionOut, CategoriaDonacionOut, PasoFuncionamientoOut, ImpactoStatsOut, DistribucionFondosOut,
                             CampoOut)
from .services import auth_service, centro_service, donacion_service, necesidad_service, static_service, routing_service
from .clients import usuarios_client


class AuthBearer(HttpBearer):
    async def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, getattr(settings, "JWT_SECRET", settings.SECRET_KEY), algorithms=["HS256"])
            request.user = payload
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None


class AdminBearer(AuthBearer):
    async def authenticate(self, request, token):
        payload = await super().authenticate(request, token)
        if payload and payload.get("rol") == "admin":
            return payload
        return None


api = NinjaAPI(title="Donatón BFF", version="1.0.0", auth=AuthBearer(),
    openapi_extra={"info": {"description": "BFF para donaton-frontend"}})


@api.exception_handler(BffError)
def on_bff_error(request, exc):
    return api.create_response(request, {"error": exc.message}, status=exc.status)

@api.exception_handler(NinjaValidationError)
def on_validation_error(request, exc):
    return api.create_response(request, {"error": str(exc)}, status=422)

@api.exception_handler(Exception)
def on_generic_error(request, exc):
    return api.create_response(request, {"error": "Error interno del servidor"}, status=500)


# ── Health ──

@api.get("/health", auth=None, response=HealthOut)
async def health(request):
    async def check(client, url_key):
        url = getattr(settings, url_key, "")
        if not url:
            return "no configurado"
        try:
            import httpx
            async with httpx.AsyncClient(timeout=3) as c:
                resp = await c.get(f"{url.rstrip('/')}/api/", params={})
                return "ok" if resp.status_code < 500 else "error"
        except Exception:
            return "error"

    servicios = {
        "usuarios": await check("usuarios", "USUARIOS_URL"),
        "logistica": await check("logistica", "LOGISTICA_URL"),
        "donaciones": await check("donaciones", "DONACIONES_URL"),
    }
    return {
        "db": "n/a (BFF sin BD de dominio)",
        "redis": "no configurado",
        "circuit_breakers": {},
        "servicios": servicios,
        "version": "1.0.0",
    }


# ── Auth ──

@api.post("/auth/login", auth=None, response=LoginOut)
async def login(request, body: LoginIn):
    return await auth_service.login(body)

@api.post("/auth/register", auth=None, response={201: UserOut})
async def register(request, body: RegisterIn):
    return await auth_service.register(body)

@api.get("/auth/me", response=UserOut)
async def me(request):
    return await auth_service.get_profile(request.user["rut"], uat=request.user.get("uat"))

@api.put("/auth/profile", response=UserOut)
async def update_profile(request, body: UserUpdateIn):
    return await auth_service.update_profile(request.user["rut"], body, uat=request.user.get("uat"))


# ── Centros ──

@api.get("/centros", auth=None, response=list[CentroOut])
async def list_centros(request):
    return await centro_service.list_all()

@api.get("/centros/{code}", auth=None, response=CentroOut)
async def get_centro(request, code: str):
    return await centro_service.get_by_code(code)

@api.post("/centros", auth=AdminBearer(), response={201: CentroOut})
async def create_centro(request, body: CentroCreate):
    return await centro_service.create(body)

@api.put("/centros/{code}", response=CentroOut)
async def update_centro(request, code: str, body: CentroUpdate):
    return await centro_service.update(code, body)

@api.get("/centros/{code}/stats", auth=None, response=CentroStatsOut)
async def get_centro_stats(request, code: str):
    return await centro_service.get_stats(code)

@api.get("/centros/{code}/inventario", auth=None, response=list[InventarioItem])
async def get_centro_inventario(request, code: str):
    return await centro_service.get_inventario(code)


@api.get("/ruta", auth=None, response=RutaOut)
async def get_ruta(request, origen_lat: float, origen_lng: float, dest_lat: float, dest_lng: float, modo: str = "driving"):
    return await routing_service.calcular_ruta(origen_lat, origen_lng, dest_lat, dest_lng, modo)


# ── Donaciones ──

@api.get("/donaciones", auth=None, response=list[DonacionOut])
async def list_donaciones(request, estado: Optional[str] = None, centro_code: Optional[str] = None, tipo: Optional[str] = None):
    return await donacion_service.list_all(estado=estado, centro_code=centro_code, tipo=tipo)

@api.get("/donaciones/{code}", auth=None, response=DonacionOut)
async def get_donacion(request, code: str):
    return await donacion_service.get_by_code(code)

@api.post("/donaciones", response={201: DonacionOut})
async def create_donacion(request, body: DonacionCreate):
    return await donacion_service.create(body, rut=request.user["rut"])

@api.patch("/donaciones/{code}/estado", response=DonacionOut)
async def update_donacion_estado(request, code: str, body: DonacionUpdate):
    return await donacion_service.update_estado(code, body.estado)

@api.delete("/donaciones/{code}", response={204: None})
async def delete_donacion(request, code: str):
    await donacion_service.delete(code)
    return 204, None

@api.get("/donaciones/stats/resumen", auth=None, response=DonacionStatsOut)
async def get_donacion_stats(request):
    return await donacion_service.get_stats()


# ── Necesidades ──

@api.get("/necesidades", auth=None, response=list[NecesidadOut])
async def list_necesidades(request, estado: Optional[str] = None, centro_code: Optional[str] = None, urgencia: Optional[str] = None):
    return await necesidad_service.list_all(estado=estado, centro_code=centro_code, urgencia=urgencia)

@api.post("/necesidades", response={201: NecesidadOut})
async def create_necesidad(request, body: NecesidadCreate):
    return await necesidad_service.create(body, rut=request.user["rut"])

# Rutas fijas (antes de {code} para evitar conflictos)

@api.get("/necesidades/ciudadanas", auth=None, response=list[NecesidadOut])
async def list_necesidades_ciudadanas(request):
    return await necesidad_service.list_ciudadanas()

@api.post("/necesidades/ciudadanas", auth=None, response={201: NecesidadOut})
async def create_necesidad_ciudadana(request, body: NecesidadCreate):
    user = getattr(request, "user", None)
    rut = "anónimo"
    if user is not None and hasattr(user, "get"):
        rut = user.get("rut", "anónimo")
    return await necesidad_service.crear_ciudadana(body, rut)

@api.patch("/necesidades/ciudadanas/{code}", auth=None, response=NecesidadOut)
async def update_necesidad_ciudadana(request, code: str, body: NecesidadUpdate):
    return await necesidad_service.actualizar_ciudadana(code, body)

@api.delete("/necesidades/ciudadanas/{code}", auth=None, response={204: None})
async def delete_necesidad_ciudadana(request, code: str):
    await necesidad_service.eliminar_ciudadana(code)
    return 204, None

@api.get("/necesidades/{code}", auth=None, response=NecesidadOut)
async def get_necesidad(request, code: str):
    return await necesidad_service.get_by_code(code)

@api.put("/necesidades/{code}", response=NecesidadOut)
async def update_necesidad(request, code: str, body: NecesidadUpdate):
    return await necesidad_service.update(code, body)

@api.post("/necesidades/{code}/activar", auth=None, response=NecesidadOut)
async def activar_necesidad(request, code: str):
    return await necesidad_service.activar(code)


# ── Propuestas ──

@api.get("/necesidades/{code}/propuestas", auth=None, response=list[PropuestaOut])
async def list_propuestas(request, code: str):
    return await necesidad_service.list_propuestas(code)

@api.post("/propuestas", response={201: PropuestaOut})
async def create_propuesta(request, body: PropuestaCreate):
    return await necesidad_service.crear_propuesta(body.necesidad_code, body.mensaje, rut=request.user["rut"])


# ── Catálogos ──

@api.get("/static/tipos-recurso", response=list[TipoRecursoOut], auth=None)
async def list_tipos_recurso(request): return await static_service.get_tipos_recurso()

@api.get("/static/unidades", response=list[UnidadOut], auth=None)
async def list_unidades(request): return await static_service.get_unidades()

@api.get("/static/equipo", response=list[EquipoOut], auth=None)
async def list_equipo(request): return await static_service.get_equipo()

@api.get("/static/gobernanza", response=list[GobernanzaOut], auth=None)
async def list_gobernanza(request): return await static_service.get_gobernanza()

@api.get("/static/hitos", response=list[HitoOut], auth=None)
async def list_hitos(request): return await static_service.get_hitos()

@api.get("/static/valores", response=list[ValorOut], auth=None)
async def list_valores(request): return await static_service.get_valores()

@api.get("/static/reportes", response=list[ReporteOut], auth=None)
async def list_reportes(request): return await static_service.get_reportes()

@api.get("/static/regiones", response=list[RegionOut], auth=None)
async def list_regiones(request): return await static_service.get_regiones()

@api.get("/static/categorias-donacion", response=list[CategoriaDonacionOut], auth=None)
async def list_categorias_donacion(request): return await static_service.get_categorias_donacion()

@api.get("/static/pasos-funcionamiento", response=list[PasoFuncionamientoOut], auth=None)
async def list_pasos_funcionamiento(request): return await static_service.get_pasos_funcionamiento()

@api.get("/static/impacto-stats", response=list[ImpactoStatsOut], auth=None)
async def list_impacto_stats(request): return await static_service.get_impacto_stats()

@api.get("/static/distribucion-fondos", response=list[DistribucionFondosOut], auth=None)
async def list_distribucion_fondos(request): return await static_service.get_distribucion_fondos()

@api.get("/static/unidades-por-tipo", auth=None)
async def list_unidades_por_tipo(request): return await static_service.get_unidades_por_tipo()

@api.get("/static/campos-por-tipo", auth=None)
async def list_campos_por_tipo(request): return await static_service.get_campos_por_tipo()



