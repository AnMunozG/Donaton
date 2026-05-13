import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from asgiref.sync import sync_to_async

from ..models import Cuenta
from ..schemas.auth import LoginIn, RegisterIn, UserUpdateIn
from ..exceptions import AuthError, ValidationError, NotFoundError


def _create_token(cuenta: Cuenta) -> str:
    payload = {
        "rut": cuenta.rut,
        "nombre": cuenta.nombre,
        "email": cuenta.email,
        "rol": cuenta.rol,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    secret = getattr(settings, "JWT_SECRET", settings.SECRET_KEY)
    return jwt.encode(payload, secret, algorithm="HS256")


async def login(data: LoginIn) -> dict:
    try:
        cuenta = await Cuenta.objects.aget(rut=data.rut)
    except Cuenta.DoesNotExist:
        raise AuthError("RUT o contraseña incorrectos")

    if not await sync_to_async(cuenta.check_password)(data.password):
        raise AuthError("RUT o contraseña incorrectos")

    if not cuenta.activo:
        raise AuthError("Cuenta desactivada")

    token = _create_token(cuenta)
    return {
        "rut": cuenta.rut,
        "nombre": cuenta.nombre,
        "email": cuenta.email,
        "rol": cuenta.rol,
        "token": token,
    }


async def register(data: RegisterIn) -> Cuenta:
    existe = await Cuenta.objects.filter(rut=data.rut).aexists()
    if existe:
        raise ValidationError("El RUT ya está registrado")

    existe_email = await Cuenta.objects.filter(email=data.email).aexists()
    if existe_email:
        raise ValidationError("El email ya está registrado")

    cuenta = Cuenta(
        rut=data.rut,
        nombre=data.nombre,
        email=data.email,
        telefono=data.telefono,
        direccion=data.direccion,
    )
    cuenta.set_password(data.password)
    await sync_to_async(cuenta.save)()
    return cuenta


async def get_profile(rut: str) -> Cuenta:
    try:
        return await Cuenta.objects.aget(rut=rut)
    except Cuenta.DoesNotExist:
        raise NotFoundError("Cuenta no encontrada")


async def update_profile(rut: str, data: UserUpdateIn) -> Cuenta:
    try:
        cuenta = await Cuenta.objects.aget(rut=rut)
    except Cuenta.DoesNotExist:
        raise NotFoundError("Cuenta no encontrada")

    update_fields = []
    for field in ["nombre", "email", "telefono", "direccion"]:
        value = getattr(data, field, None)
        if value is not None:
            setattr(cuenta, field, value)
            update_fields.append(field)

    if update_fields:
        await sync_to_async(cuenta.save)(update_fields=update_fields)

    return cuenta
