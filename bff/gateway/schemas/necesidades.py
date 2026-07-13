from ninja import Schema
from typing import Optional, Any
from datetime import datetime
from pydantic import field_validator


class NecesidadCreate(Schema):
    centroId: int
    recurso: str  # nombre tipo recurso ("Alimentos no perecibles", etc.)
    cantidad: int  # cantidad_requerida
    unidad: str  # nombre unidad
    descripcion: str = ""
    urgencia: str = "Media"
    reportadoPor: str = ""
    estado: str = "Activa"
    categoria: str = ""
    fecha_limite: Optional[str] = None
    detalles: dict = {}

    @field_validator("centroId", mode="before")
    @classmethod
    def validate_centro_id(cls, v):
        if v is not None:
            try:
                int(v)
            except (ValueError, TypeError):
                raise ValueError(f"centroId debe ser numérico, recibido: '{v}'")
        return int(v) if v is not None and v != "" else v


class NecesidadUpdate(Schema):
    cantidad: Optional[int] = None
    urgencia: Optional[str] = None
    estado: Optional[str] = None
    descripcion: Optional[str] = None
    reportadoPor: Optional[str] = None
    categoria: Optional[str] = None
    fecha_limite: Optional[str] = None
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
    categoria: str = "OTROS"
    fecha_limite: Optional[str] = None
    detalles: dict = {}


class ActivarNecesidadIn(Schema):
    urgencia: str = None


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
