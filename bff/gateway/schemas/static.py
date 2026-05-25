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


class HealthOut(Schema):
    db: str
    redis: str
    circuit_breakers: dict
    servicios: dict = {}
    version: str
