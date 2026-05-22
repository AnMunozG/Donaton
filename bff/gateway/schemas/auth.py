from ninja import Schema
from typing import Optional
from datetime import datetime


class LoginIn(Schema):
    rut: str
    password: str


class LoginOut(Schema):
    rut: str
    nombre: str
    email: str
    rol: str
    token: str


class RegisterIn(Schema):
    rut: str
    nombre: str
    email: str
    password: str
    telefono: str = ""
    direccion: str = ""


class UserOut(Schema):
    rut: str
    nombre: str
    email: str
    rol: str
    telefono: str
    direccion: str
    activo: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateIn(Schema):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
