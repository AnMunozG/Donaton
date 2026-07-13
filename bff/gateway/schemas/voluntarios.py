from ninja import Schema
from pydantic import ConfigDict
from typing import Optional


class VoluntarioCreate(Schema):
    disponibilidad: str = "emergencia"
    habilidades: list[str] = []
    centro_id: Optional[str] = None


class VoluntarioUpdate(Schema):
    disponibilidad: Optional[str] = None
    habilidades: Optional[list[str]] = None


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
    fecha_registro: str
    horas_acumuladas: int = 0
    centros: list["VoluntarioCentroOut"] = []


class VoluntarioListOut(Schema):
    id: str
    rut: str
    nombre: str = ""
    email: str = ""
    disponibilidad: str
    habilidades: list[str]
    fecha_registro: str
    horas_acumuladas: int = 0
    centros: list["VoluntarioCentroOut"] = []


class VoluntarioCentroCreate(Schema):
    centro_id: str


class VoluntarioCentroUpdate(Schema):
    estado: str


class VoluntarioCentroOut(Schema):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: str
    voluntario: str
    centro_id: str
    estado: str
    fecha_registro: str
    horas_acumuladas: int = 0


class RegistrarHorasIn(Schema):
    horas: int
    descripcion: str = ""
    centro_id: str = ""


class RegistroHorasOut(Schema):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: str
    voluntario: str
    centro_id: str
    horas: int
    descripcion: str
    registrado_por_rut: str
    fecha: str


class HorasVoluntarioOut(Schema):
    horas_acumuladas: int
    horas_por_centro: dict = {}
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


class NotificacionCreate(Schema):
    voluntario_id: str
    titulo: str
    mensaje: str


class NotificacionOut(Schema):
    model_config = ConfigDict(coerce_numbers_to_str=True)
    id: str
    voluntario: str
    titulo: str
    mensaje: str
    leida: bool
    enviado_por_rut: str
    fecha_creacion: str
