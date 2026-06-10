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


class RegionOut(Schema):
    nombre: str


class CategoriaDonacionOut(Schema):
    code: str
    nombre: str
    icono: str
    descripcion: str


class PasoFuncionamientoOut(Schema):
    code: str
    paso: int
    titulo: str
    descripcion: str


class ImpactoStatsOut(Schema):
    code: str
    valor: str
    label: str
    icono: str


class DistribucionFondosOut(Schema):
    code: str
    label: str
    porcentaje: int


class CampoOut(Schema):
    name: str
    label: str
    type: str
    options: Optional[list[str]] = None
    placeholder: Optional[str] = None


class HealthOut(Schema):
    db: str
    redis: str
    circuit_breakers: dict
    servicios: dict = {}
    version: str
