from ninja import Schema
from typing import Optional
from datetime import datetime


class LogroOut(Schema):
    id: int
    codigo: str
    nombre: str
    descripcion: str
    icono: str
    categoria: str
    orden: int


class LogroUsuarioOut(Schema):
    id: int
    logro: LogroOut
    codigo: str
    fecha_obtenido: datetime
    progreso: float


class VerificarLogrosIn(Schema):
    total_donaciones: int = 0
    centros_distintos: int = 0
    total_kg: float = 0
    max_items_una_donacion: int = 0
