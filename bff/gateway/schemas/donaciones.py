from ninja import Schema
from typing import Optional, Any
from datetime import datetime
from pydantic import field_validator


class DonacionCreate(Schema):
    tipo: str  # "Alimentos no perecibles", "Ropa y abrigo", "Donación Monetaria", etc.
    cantidad: float
    unidad: str  # nombre de unidad (kg, unidades, etc.)
    origen: str = ""  # nombre o RUT del donante
    centroId: str  # centro code
    fecha: str = ""
    estado: str = "Recibido"
    comprobante: str = ""
    detalles: dict = {}


class DonacionUpdate(Schema):
    estado: Optional[str] = None


class DonacionOut(Schema):
    id: str  # code
    tipo: str
    cantidad: str  # string formateada (ej: "50")
    unidad: str
    origen: str
    centroId: str
    centro: str = ""  # nombre del centro (se resuelve si está disponible)
    fecha: str
    estado: str
    detalles: dict = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("id", "cantidad", mode="before")
    @classmethod
    def coerce_to_str(cls, v):
        if v is not None:
            return str(v)
        return v


class DonacionStatsOut(Schema):
    total_donaciones: int
    total_monto: float
    total_beneficiarios: int
    centros_activos: int
    por_estado: dict
    por_tipo: dict
