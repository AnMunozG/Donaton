from ninja import Schema
from typing import Optional
from datetime import datetime, date


class TipoRecursoOut(Schema):
    code: str
    nombre: str
    descripcion: str
    activo: bool


class UnidadOut(Schema):
    code: str
    nombre: str
    abreviatura: str


class EquipoOut(Schema):
    code: str
    nombre: str
    cargo: str
    email: str
    foto_url: str
    activo: bool


class GobernanzaOut(Schema):
    code: str
    nombre: str
    cargo: str
    img_url: str


class HitoOut(Schema):
    code: str
    year: str
    titulo: str
    descripcion: str
    tipo: str


class ValorOut(Schema):
    code: str
    titulo: str
    descripcion: str
    icono: str


class ReporteOut(Schema):
    code: str
    titulo: str
    fecha: str
    tipo: str
    size: str
    icono: str
    color: str


class EnvioOut(Schema):
    id: str  # code
    donacionId: Optional[str] = None
    centroId: str
    centro: str
    destino: str
    fechaSalida: Optional[str] = None
    fechaEntrega: Optional[str] = None
    estado: str
    transportista: str


class EnvioCreate(Schema):
    donacionId: Optional[str] = None
    centroId: str
    destino: str
    fechaSalida: Optional[str] = None
    transportista: str = ""


class EnvioUpdate(Schema):
    estado: Optional[str] = None
    fechaSalida: Optional[str] = None
    fechaEntrega: Optional[str] = None
    transportista: Optional[str] = None
    destino: Optional[str] = None


class HealthOut(Schema):
    db: str
    redis: str
    circuit_breakers: dict
    servicios: dict = {}
    version: str
