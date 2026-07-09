from ninja import Schema
from typing import Optional
from datetime import datetime


class AgradecimientoCreate(Schema):
    centro_id: str
    usuario_rut: str
    donacion_id: Optional[str] = None
    mensaje: str


class AgradecimientoOut(Schema):
    id: int
    centro_id: str
    centro_nombre: str = ""
    usuario_rut: str
    donacion_id: Optional[str] = None
    mensaje: str
    fecha: datetime
