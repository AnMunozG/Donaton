from ninja import Schema
from typing import Optional, Any
from datetime import datetime


class Coordenadas(Schema):
    lat: float
    lng: float


class InventarioItem(Schema):
    tipo: str
    cantidad: str


class CentroCreate(Schema):
    nombre: str
    region: str = "Metropolitana"
    direccion: str
    telefono: str = ""
    coordenadas: Optional[Coordenadas] = None
    capacidadTotal: int = 0
    encargado_rut: Optional[str] = None


class CentroUpdate(Schema):
    nombre: Optional[str] = None
    region: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    coordenadas: Optional[Coordenadas] = None
    capacidadTotal: Optional[int] = None
    inventario: Optional[list[InventarioItem]] = None
    estado: Optional[str] = None


class CentroOut(Schema):
    id: str  # code
    nombre: str
    region: str
    direccion: str
    coordenadas: Optional[Coordenadas] = None
    encargado: Optional[str] = None  # nombre del encargado
    telefono: str
    capacidadTotal: int
    capacidadUsada: float
    inventario: list[InventarioItem] = []
    estado: str


class CentroStatsOut(Schema):
    id: str
    nombre: str
    total_donaciones: int
    total_necesidades: int
    capacidad_usada: float
