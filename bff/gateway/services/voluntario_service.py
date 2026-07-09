from ..schemas.voluntarios import VoluntarioOut, VoluntarioListOut, HorasVoluntarioOut
from ..exceptions import NotFoundError, ValidationError, AuthError
from ..clients.voluntarios_client import VoluntariosClient
from ..clients.usuarios_client import UsuariosClient

voluntarios_client = VoluntariosClient()
usuarios_client = UsuariosClient()


def _estado_desde_voluntario(v: dict) -> str:
    return v.get("estado", "pendiente")


async def _enrich(voluntario: dict, uat: str = None) -> dict:
    rut = voluntario.get("rut", "")
    datos_usuario = {"nombre": "", "email": "", "telefono": ""}
    if rut and uat:
        try:
            users = await usuarios_client.listar_usuarios(token=uat)
            user = next((u for u in (users or []) if u.get("rut") == rut), None)
            if user:
                nombre = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
                datos_usuario = {
                    "nombre": nombre or user.get("username", ""),
                    "email": user.get("email", ""),
                    "telefono": user.get("telefono", ""),
                }
        except Exception:
            pass
    return {
        "id": str(voluntario.get("id", "")),
        "rut": rut,
        "nombre": datos_usuario["nombre"],
        "email": datos_usuario["email"],
        "telefono": datos_usuario["telefono"],
        "disponibilidad": voluntario.get("disponibilidad", "emergencia"),
        "habilidades": voluntario.get("habilidades", []),
        "centro_preferido": voluntario.get("centro_preferido", ""),
        "estado": _estado_desde_voluntario(voluntario),
        "fecha_registro": str(voluntario.get("fecha_registro", "")),
        "horas_acumuladas": int(voluntario.get("horas_acumuladas", 0)),
    }


def _list_to_out(voluntario: dict) -> dict:
    return {
        "id": str(voluntario.get("id", "")),
        "rut": voluntario.get("rut", ""),
        "nombre": "",
        "disponibilidad": voluntario.get("disponibilidad", "emergencia"),
        "habilidades": voluntario.get("habilidades", []),
        "centro_preferido": voluntario.get("centro_preferido", ""),
        "estado": _estado_desde_voluntario(voluntario),
        "fecha_registro": str(voluntario.get("fecha_registro", "")),
        "horas_acumuladas": int(voluntario.get("horas_acumuladas", 0)),
    }


async def list_all(user=None, uat: str = None) -> list:
    try:
        params = {"estado": "activo"}
        is_backoffice = isinstance(user, dict) and user.get("rol") in ("admin", "encargado")
        if is_backoffice:
            if user.get("rol") == "encargado":
                params = {"centro_preferido": user.get("centro_acopio_id", "")}
            else:
                params = {}

        data = await voluntarios_client.listar_voluntarios(params=params)
        items = data if isinstance(data, list) else []
        if is_backoffice and uat:
            result = []
            for v in items:
                enriched = await _enrich(v, uat=uat)
                result.append(VoluntarioOut(**enriched))
            return result
        return [VoluntarioListOut(**(_list_to_out(v))) for v in items]
    except Exception:
        return []


async def get_by_code(code: str, uat: str = None) -> VoluntarioOut:
    data = await voluntarios_client.obtener_voluntario(code)
    if not data or "error" in data:
        raise NotFoundError("Voluntario no encontrado")
    enriched = await _enrich(data, uat=uat)
    return VoluntarioOut(**enriched)


async def get_by_rut(rut: str, uat: str = None) -> VoluntarioOut | None:
    data = await voluntarios_client.obtener_voluntario_por_rut(rut)
    if not data or "error" in data:
        return None
    enriched = await _enrich(data, uat=uat)
    return VoluntarioOut(**enriched)


async def create(body, rut: str, uat: str = None) -> VoluntarioOut:
    existente = await voluntarios_client.obtener_voluntario_por_rut(rut)
    if existente and "error" not in existente:
        raise ValidationError(f"El usuario {rut} ya está registrado como voluntario")

    users = await usuarios_client.listar_usuarios(token=uat)
    user = next((u for u in (users or []) if u.get("rut") == rut), None)
    if not user:
        raise ValidationError("El RUT no corresponde a un usuario registrado")

    data = {
        "rut": rut,
        "disponibilidad": body.disponibilidad,
        "habilidades": body.habilidades,
        "centro_preferido": body.centro_preferido,
        "estado": "pendiente",
    }
    created = await voluntarios_client.crear_voluntario(data)
    if "error" in created:
        raise ValidationError(created.get("error", "Error al crear voluntario"))
    enriched = await _enrich(created, uat=uat)
    return VoluntarioOut(**enriched)


async def update(code: str, body, user: dict, uat: str = None) -> VoluntarioOut:
    if user.get("rol") not in ("admin", "encargado") and user.get("rut") != code:
        raise AuthError("No tienes permiso para modificar este voluntario")

    data = {}
    if body.disponibilidad is not None:
        data["disponibilidad"] = body.disponibilidad
    if body.habilidades is not None:
        data["habilidades"] = body.habilidades
    if body.centro_preferido is not None:
        data["centro_preferido"] = body.centro_preferido

    updated = await voluntarios_client.actualizar_voluntario(code, data)
    if "error" in updated:
        raise ValidationError(updated.get("error", "Error al actualizar voluntario"))
    enriched = await _enrich(updated, uat=uat)
    return VoluntarioOut(**enriched)


async def cambiar_estado(code: str, nuevo_estado: str, user: dict, uat: str = None) -> VoluntarioOut:
    if user.get("rol") not in ("admin", "encargado"):
        raise AuthError("No tienes permiso para cambiar el estado de voluntarios")
    if nuevo_estado not in ("activo", "inactivo"):
        raise ValidationError("Estado inválido. Valores permitidos: activo, inactivo")

    data = {"estado": nuevo_estado}
    updated = await voluntarios_client.actualizar_voluntario(code, data)
    if "error" in updated:
        raise ValidationError(updated.get("error", "Error al cambiar estado"))
    enriched = await _enrich(updated, uat=uat)
    return VoluntarioOut(**enriched)


async def delete(code: str, user: dict) -> None:
    if user.get("rol") != "admin":
        raise AuthError("Solo administradores pueden eliminar voluntarios")
    result = await voluntarios_client.eliminar_voluntario(code)
    if result and "error" in result:
        raise ValidationError(result.get("error", "Error al eliminar voluntario"))


async def registrar_horas(code: str, body, user: dict, uat: str = None) -> dict:
    if user.get("rol") not in ("admin", "encargado") and user.get("rut") != code:
        raise AuthError("No tienes permiso para registrar horas de este voluntario")

    data = {
        "horas": body.horas,
        "descripcion": body.descripcion,
        "registrado_por_rut": user.get("rut", ""),
    }
    result = await voluntarios_client.registrar_horas(code, data)
    if "error" in result:
        raise ValidationError(result.get("error", "Error al registrar horas"))
    return result


async def listar_horas(code: str, user: dict, uat: str = None) -> HorasVoluntarioOut:
    data = await voluntarios_client.listar_horas(code)
    if "error" in data:
        raise NotFoundError("Voluntario no encontrado")
    return HorasVoluntarioOut(**data)
