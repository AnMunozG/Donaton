from ninja import Schema
from typing import Optional
from datetime import datetime


class ImpactoPorMes(Schema):
    mes: str
    cantidad: int
    total_kg: float = 0


class CentroImpactado(Schema):
    id: str
    nombre: str
    region: str = ""
    lat: Optional[float] = None
    lng: Optional[float] = None
    total_donaciones: int = 0
    total_kg: float = 0


class ImpactoOut(Schema):
    total_donaciones: int
    total_kg: float
    total_items: int
    total_monetario: float
    centros_distintos: int
    por_tipo: dict = {}
    por_mes: list[ImpactoPorMes] = []
    centros: list[CentroImpactado] = []
    ultima_donacion: Optional[str] = None
