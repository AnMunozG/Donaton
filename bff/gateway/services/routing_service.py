import httpx
from urllib.parse import urlencode

from ..schemas.centros import RutaOut, RutaPuntoOut
from ..exceptions import BffError

OSRM_BASE = "https://router.project-osrm.org/route/v1"


async def calcular_ruta(origen_lat: float, origen_lng: float,
                        dest_lat: float, dest_lng: float,
                        modo: str = "driving") -> RutaOut:
    coords = f"{origen_lng},{origen_lat};{dest_lng},{dest_lat}"
    params = urlencode({"geometries": "geojson", "overview": "full", "steps": "false", "alternatives": "false"})
    url = f"{OSRM_BASE}/{modo}/{coords}?{params}"

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, headers={"User-Agent": "Donaton/1.0"})
        body = resp.json()

    if body.get("code") != "Ok":
        raise BffError(body.get("message", body.get("code", "Error al calcular ruta")))

    routes = body.get("routes")
    if not routes:
        raise BffError("No se encontró una ruta entre los puntos seleccionados")

    route = routes[0]
    coords_geo = route["geometry"]["coordinates"]
    line = [RutaPuntoOut(lat=c[1], lng=c[0]) for c in coords_geo]

    return RutaOut(
        line=line,
        distancia=route["distance"],
        duracion=route["duration"],
    )
