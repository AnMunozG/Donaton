from ninja import Schema
from typing import Optional, Any
from datetime import datetime
from pydantic import field_validator


class DonacionCreate(Schema):
    tipo: str  # "Alimentos no perecibles", "Ropa y abrigo", "Donación Monetaria", etc.
    cantidad: int
    unidad: str  # nombre de unidad (kg, unidades, etc.)
    origen: str = ""  # nombre o RUT del donante
    centroId: str  # centro code
    fecha: str = ""
    estado: str = "Donación Registrada"
    comprobante: str = ""
    detalles: dict = {}

    @field_validator("fecha", mode="before")
    @classmethod
    def validate_fecha(cls, v):
        if v and v != "":
            from datetime import date
            try:
                date.fromisoformat(v)
            except (ValueError, TypeError):
                raise ValueError(f"Fecha inválida: '{v}'. Use formato YYYY-MM-DD.")
        return v


class ItemDonacionCreate(Schema):
    tipo: str
    cantidad: float
    unidad: str
    detalles: dict = {}


class DonacionMultiCreate(Schema):
    items: list[ItemDonacionCreate]
    origen: str = ""
    centroId: str
    fecha: str = ""
    estado: str = "Donación Registrada"
    notas: str = ""
    direccion_retiro: str = ""
    fecha_retiro: str = ""
    detalles: dict = {}

    @field_validator("fecha", mode="before")
    @classmethod
    def validate_fecha(cls, v):
        if v and v != "":
            from datetime import date
            try:
                date.fromisoformat(v)
            except (ValueError, TypeError):
                raise ValueError(f"Fecha inválida: '{v}'. Use formato YYYY-MM-DD.")
        return v


class DonacionUpdate(Schema):
    estado: Optional[str] = None


class ItemDonacionOut(Schema):
    id: str
    tipo: str
    cantidad: str
    unidad: str
    detalles: dict = {}

    @field_validator("id", "cantidad", mode="before")
    @classmethod
    def coerce_to_str(cls, v):
        if v is not None:
            return str(v)
        return v


class DonacionOut(Schema):
    id: str  # code
    tipo: Optional[str] = None
    cantidad: Optional[str] = None  # string formateada (ej: "50")
    unidad: Optional[str] = None
    origen: str
    centroId: str
    centro: str = ""  # nombre del centro (se resuelve si está disponible)
    fecha: str
    estado: str
    detalles: dict = {}
    items: list[ItemDonacionOut] = []
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
