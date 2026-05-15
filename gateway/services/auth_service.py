import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from ..clients import usuarios_client
from ..schemas.auth import LoginIn, RegisterIn, UserUpdateIn
from ..exceptions import AuthError, ValidationError


def _rol_from_user(user: dict) -> str:
    return "admin" if user.get("is_staff", False) else "donante"


def _crear_bff_token(user: dict, uat: str = "") -> str:
    nombre = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    payload = {
        "rut": user.get("rut", ""),
        "nombre": nombre or user.get("username", ""),
        "email": user.get("email", ""),
        "rol": _rol_from_user(user),
        "uat": uat,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    secret = getattr(settings, "JWT_SECRET", settings.SECRET_KEY)
    return jwt.encode(payload, secret, algorithm="HS256")


async def login(data: LoginIn) -> dict:
    # 1. Pedir token al microservicio de Usuarios
    token_resp = await usuarios_client.login(data.rut, data.password)
    if "error" in token_resp or "access" not in token_resp:
        raise AuthError("RUT o contraseña incorrectos")

    uat = token_resp["access"]  # usuarios access token

    # 2. Extraer user_id del JWT de Usuarios SIN validar firma
    #    (está firmado con el secret de Usuarios, no el del BFF)
    payload = jwt.decode(uat, options={"verify_signature": False})
    user_id = payload.get("user_id")
    if not user_id:
        raise AuthError("Token inválido: sin user_id")

    # 3. Obtener perfil desde Usuarios usando su propio token
    user = await usuarios_client.obtener_usuario(user_id, token=uat)
    if not user or "error" in user or "detail" in user:
        raise AuthError("Error al obtener perfil de usuario")

    # 4. Crear JWT del BFF (incluye uat para futuras llamadas a Usuarios)
    bff_token = _crear_bff_token(user, uat=uat)

    nombre = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    return {
        "rut": user.get("rut", ""),
        "nombre": nombre or user.get("username", ""),
        "email": user.get("email", ""),
        "rol": _rol_from_user(user),
        "token": bff_token,
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

    now = datetime.now(timezone.utc)
    return {
        "rut": resp.get("rut", data.rut),
        "nombre": data.nombre,
        "email": data.email,
        "rol": "donante",
        "telefono": "",
        "direccion": "",
        "activo": True,
        "created_at": now,
        "updated_at": now,
    }


async def get_profile(rut: str, uat: str = None) -> dict:
    """Obtiene perfil desde Usuarios. Requiere uat (access token de Usuarios)."""
    if not uat:
        raise AuthError("Sesión expirada")

    users = await usuarios_client.listar_usuarios(token=uat)
    if isinstance(users, list):
        user = next((u for u in users if u.get("rut") == rut), None)
        if user:
            return _user_from_usuarios(user)
    raise AuthError("Usuario no encontrado")


async def update_profile(rut: str, data: UserUpdateIn, uat: str = None) -> dict:
    if not uat:
        raise AuthError("Sesión expirada")

    users = await usuarios_client.listar_usuarios(token=uat)
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
        updated = await usuarios_client.actualizar_usuario(user["id"], payload, token=uat)
        return _user_from_usuarios(updated)
    return _user_from_usuarios(user)


def _user_from_usuarios(user: dict) -> dict:
    nombre = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    date_joined = user.get("date_joined") or datetime.now(timezone.utc)
    return {
        "rut": user.get("rut", ""),
        "nombre": nombre or user.get("username", ""),
        "email": user.get("email", ""),
        "rol": _rol_from_user(user),
        "telefono": "",
        "direccion": "",
        "activo": user.get("is_active", True),
        "created_at": date_joined,
        "updated_at": date_joined,
    }
