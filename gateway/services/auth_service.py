import jwt
from django.conf import settings
from ..clients import usuarios_client
from ..schemas.auth import LoginIn, RegisterIn, UserUpdateIn
from ..exceptions import AuthError, ValidationError


def _decode_token(token: str) -> dict:
    secret = getattr(settings, "JWT_SECRET", settings.SECRET_KEY)
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expirado")
    except jwt.InvalidTokenError:
        raise AuthError("Token inválido")


async def login(data: LoginIn) -> dict:
    token_resp = await usuarios_client.login(data.rut, data.password)
    if "error" in token_resp or "access" not in token_resp:
        raise AuthError("RUT o contraseña incorrectos")

    access_token = token_resp["access"]
    payload = _decode_token(access_token)
    user_id = payload.get("user_id")

    user = await usuarios_client.obtener_usuario(user_id)
    if not user or "error" in user:
        raise AuthError("Error al obtener perfil")

    nombre = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    return {
        "rut": user.get("rut", data.rut),
        "nombre": nombre or user.get("username", ""),
        "email": user.get("email", ""),
        "rol": "donante",  # TODO: cuando usuarios service tenga roles
        "token": access_token,
    }


async def register(data: RegisterIn) -> dict:
    resp = await usuarios_client.registrar(
        rut=data.rut,
        email=data.email,
        first_name=data.nombre,
        last_name="",
        password=data.password,
    )
    if "error" in resp:
        raise ValidationError(resp.get("error", "Error al registrar"))
    if "mensaje" in resp and "siguiente_paso" in resp:
        pass

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    return {
        "rut": resp.get("rut", data.rut),
        "nombre": data.nombre,
        "email": data.email,
        "rol": "donante",
        "telefono": "",
        "direccion": "",
        "activo": True,
        "created_at": resp.get("date_joined") or now,
        "updated_at": resp.get("date_joined") or now,
    }


async def get_profile(rut: str) -> dict:
    users = await usuarios_client.listar_usuarios()
    if isinstance(users, list):
        user = next((u for u in users if u.get("rut") == rut), None)
        if user:
            return _user_from_usuarios(user)
    raise AuthError("Usuario no encontrado")


async def update_profile(rut: str, data: UserUpdateIn) -> dict:
    users = await usuarios_client.listar_usuarios()
    user = None
    for u in (users or []):
        if u.get("rut") == rut:
            user = u
            break
    if not user:
        raise AuthError("Usuario no encontrado")

    payload = {}
    if data.nombre is not None:
        payload["first_name"] = data.nombre
    if data.email is not None:
        payload["email"] = data.email

    if payload:
        updated = await usuarios_client._request("PATCH", f"/api/usuarios/{user['id']}/", json=payload)
        return _user_from_usuarios(updated)
    return _user_from_usuarios(user)


def _user_from_usuarios(user: dict) -> dict:
    from datetime import datetime, timezone
    nombre = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    date_joined = user.get("date_joined") or datetime.now(timezone.utc)
    return {
        "rut": user.get("rut", ""),
        "nombre": nombre or user.get("username", ""),
        "email": user.get("email", ""),
        "rol": "donante",
        "telefono": "",
        "direccion": "",
        "activo": user.get("is_active", True),
        "created_at": date_joined,
        "updated_at": date_joined,
    }
