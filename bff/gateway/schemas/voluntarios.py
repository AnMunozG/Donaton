from ninja import Schema
from typing import Optional


class VoluntarioCreate(Schema):
    disponibilidad: str = "emergencia"
    habilidades: list[str] = []
    centro_preferido: str = ""


class VoluntarioUpdate(Schema):
    disponibilidad: Optional[str] = None
    habilidades: Optional[list[str]] = None
    centro_preferido: Optional[str] = None


class CambiarEstadoVoluntarioIn(Schema):
    estado: str  # "activo" | "inactivo"


class VoluntarioOut(Schema):
    id: str
    rut: str
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    disponibilidad: str
    habilidades: list[str]
    centro_preferido: str
    estado: str = "pendiente"
    fecha_registro: str
    horas_acumuladas: int = 0


class VoluntarioListOut(Schema):
    id: str
    rut: str
    nombre: str = ""
    disponibilidad: str
    habilidades: list[str]
    centro_preferido: str
    estado: str = "pendiente"
    fecha_registro: str
    horas_acumuladas: int = 0


class RegistrarHorasIn(Schema):
    horas: int
    descripcion: str = ""
    registrado_por_rut: str


class RegistroHorasOut(Schema):
    id: str
    voluntario: int
    horas: int
    descripcion: str
    registrado_por_rut: str
    fecha: str


class HorasVoluntarioOut(Schema):
    horas_acumuladas: int
    registros: list[RegistroHorasOut]


class AsignacionVoluntarioCreate(Schema):
    necesidad_id: int
    estado: str = "propuesto"


class AsignacionVoluntarioOut(Schema):
    id: str
    voluntario: int
    necesidad_id: int
    estado: str
    fecha_asignacion: str
    fecha_actualizacion: str
