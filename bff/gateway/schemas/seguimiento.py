from ninja import Schema
from typing import Optional
from datetime import datetime


class SeguirCentroIn(Schema):
    centro_id: str


class SeguimientoOut(Schema):
    centro_id: str
    centro_nombre: str = ""
    fecha_inicio: datetime
    activo: bool
