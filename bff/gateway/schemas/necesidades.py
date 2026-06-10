from ninja import Schema
from typing import Optional, Any
from datetime import datetime


class NecesidadCreate(Schema):
    centroId: str
    recurso: str  # nombre tipo recurso ("Alimentos no perecibles", etc.)
    cantidad: float  # cantidad_requerida
    unidad: str  # nombre unidad
    descripcion: str = ""
    urgencia: str = "Media"
    reportadoPor: str = ""
    estado: str = "Activa"
    fecha_limite: Optional[str] = None
    detalles: dict = {}


class NecesidadUpdate(Schema):
    cantidad: Optional[float] = None
    urgencia: Optional[str] = None
    estado: Optional[str] = None
    descripcion: Optional[str] = None
    reportadoPor: Optional[str] = None
    detalles: Optional[dict] = None


class NecesidadOut(Schema):
    id: str  # code
    recurso: str  # nombre tipo recurso
    cantidad: float  # cantidad_requerida
    donado: float  # cantidad_recibida
    descripcion: str
    unidad: str
    fecha: str  # created_at as iso
    urgencia: str
    estado: str
    centroId: str
    centro: str  # nombre centro
    reportadoPor: str
    detalles: dict = {}


class PropuestaCreate(Schema):
    necesidad_code: str
    mensaje: str


class PropuestaOut(Schema):
    code: str
    necesidad_code: str
    usuario_rut: str
    usuario_nombre: str
    mensaje: str
    estado: str
    created_at: datetime
    updated_at: datetime
