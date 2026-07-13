from ..schemas.voluntarios import (
    VoluntarioOut, VoluntarioListOut, HorasVoluntarioOut,
    RegistroHorasOut, VoluntarioCentroOut, NotificacionOut,
)
from ..exceptions import NotFoundError, ValidationError, AuthError
from ..clients import voluntarios_client, usuarios_client, logistica_client


def _estado_desde_voluntario(v: dict) -> str:
    centros = v.get("centros", [])
    if any(c.get("estado") == "activo" for c in centros):
        return "activo"
    if any(c.get("estado") == "pendiente" for c in centros):
        return "pendiente"
    return "sin centro"


def _centro_to_out(c: dict) -> dict:
    return {
        "id": str(c.get("id", "")),
        "voluntario": str(c.get("voluntario", "")),
        "centro_id": str(c.get("centro_id", "")),
        "estado": c.get("estado", "pendiente"),
        "fecha_registro": str(c.get("fecha_registro", "")),
        "horas_acumuladas": int(c.get("horas_acumuladas", 0)),
    }


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
    centros_raw = voluntario.get("centros", [])
    centros_out = [_centro_to_out(c) for c in centros_raw]
    return {
        "id": str(voluntario.get("id", "")),
        "rut": rut,
        "nombre": datos_usuario["nombre"],
        "email": datos_usuario["email"],
        "telefono": datos_usuario["telefono"],
        "disponibilidad": voluntario.get("disponibilidad", "emergencia"),
        "habilidades": voluntario.get("habilidades", []),
        "fecha_registro": str(voluntario.get("fecha_registro", "")),
        "horas_acumuladas": int(voluntario.get("horas_acumuladas", 0)),
        "centros": centros_out,
    }


async def _enrich_with_centros(voluntario: dict, uat: str = None) -> dict:
    enriched = await _enrich(voluntario, uat=uat)
    vol_id = voluntario.get("id")
    if vol_id:
        try:
            centros = await voluntarios_client.listar_voluntario_centros(
                params={"voluntario_id": vol_id}
            )
            enriched["centros"] = [_centro_to_out(c) for c in centros]
        except Exception:
            pass
    return enriched


async def list_all(user=None, uat: str = None, centro_id: str = None, disponibilidad: str = None, habilidad: str = None) -> list:
    try:
        params = {}
        is_backoffice = isinstance(user, dict) and user.get("rol") in ("admin", "encargado")
        if is_backoffice:
            if user.get("rol") == "encargado":
                params["centro_id"] = user.get("centro_acopio_id", "")
        if centro_id:
            params["centro_id"] = centro_id
        if disponibilidad:
            params["disponibilidad"] = disponibilidad
        if habilidad:
            params["habilidad"] = habilidad

        data = await voluntarios_client.listar_voluntarios(params=params)
        items = data if isinstance(data, list) else []

        result = []
        for v in items:
            enriched = await _enrich_with_centros(v, uat=uat if is_backoffice else None)
            if is_backoffice:
                result.append(VoluntarioOut(**enriched))
            else:
                result.append(VoluntarioListOut(**enriched))
        return result
    except Exception:
        return []


async def get_by_code(code: str, uat: str = None) -> VoluntarioOut:
    data = await voluntarios_client.obtener_voluntario(code)
    if not data or "error" in data:
        raise NotFoundError("Voluntario no encontrado")
    enriched = await _enrich_with_centros(data, uat=uat)
    return VoluntarioOut(**enriched)


async def get_by_rut(rut: str, uat: str = None) -> VoluntarioOut | None:
    data = await voluntarios_client.obtener_voluntario_por_rut(rut)
    if not data or "error" in data:
        return None
    enriched = await _enrich_with_centros(data, uat=uat)
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
    }
    created = await voluntarios_client.crear_voluntario(data)
    if "error" in created:
        raise ValidationError(created.get("error", "Error al crear voluntario"))

    if body.centro_id:
        try:
            centro = await logistica_client.obtener_centro(int(body.centro_id))
            if not centro or "error" in centro:
                raise ValidationError(f"El centro {body.centro_id} no existe en logística")
        except (ValueError, TypeError):
            raise ValidationError(f"El ID del centro '{body.centro_id}' no es válido")
        except ValidationError:
            raise
        except Exception:
            pass

        vc_data = {
            "voluntario": int(created.get("id", 0)),
            "centro_id": body.centro_id,
        }
        await voluntarios_client.crear_voluntario_centro(vc_data)

    enriched = await _enrich_with_centros(created, uat=uat)
    return VoluntarioOut(**enriched)


async def update(code: str, body, user: dict, uat: str = None) -> VoluntarioOut:
    if user.get("rol") not in ("admin", "encargado"):
        existing = await voluntarios_client.obtener_voluntario(code)
        if not existing or "error" in existing:
            raise NotFoundError("Voluntario no encontrado")
        if user.get("rut") != existing.get("rut"):
            raise AuthError("No tienes permiso para modificar este voluntario")

    data = {}
    if body.disponibilidad is not None:
        data["disponibilidad"] = body.disponibilidad
    if body.habilidades is not None:
        data["habilidades"] = body.habilidades

    updated = await voluntarios_client.actualizar_voluntario(code, data)
    if "error" in updated:
        raise ValidationError(updated.get("error", "Error al actualizar voluntario"))
    enriched = await _enrich_with_centros(updated, uat=uat)
    return VoluntarioOut(**enriched)


async def cambiar_estado(code: str, nuevo_estado: str, user: dict, uat: str = None) -> VoluntarioOut:
    if user.get("rol") not in ("admin", "encargado"):
        raise AuthError("No tienes permiso para cambiar el estado de voluntarios")
    if nuevo_estado not in ("activo", "inactivo"):
        raise ValidationError("Estado inválido. Valores permitidos: activo, inactivo")

    voluntario = await voluntarios_client.obtener_voluntario(code)
    if not voluntario or "error" in voluntario:
        raise NotFoundError("Voluntario no encontrado")

    centros = voluntario.get("centros", [])
    for vc in centros:
        if vc.get("id"):
            await voluntarios_client.actualizar_voluntario_centro(str(vc["id"]), {"estado": nuevo_estado})

    enriched = await _enrich_with_centros(voluntario, uat=uat)
    return VoluntarioOut(**enriched)


async def delete(code: str, user: dict) -> None:
    if user.get("rol") != "admin":
        raise AuthError("Solo administradores pueden eliminar voluntarios")
    result = await voluntarios_client.eliminar_voluntario(code)
    if result and "error" in result:
        raise ValidationError(result.get("error", "Error al eliminar voluntario"))


async def registrar_horas(code: str, body, user: dict, uat: str = None) -> RegistroHorasOut:
    if user.get("rol") not in ("admin", "encargado"):
        existing = await voluntarios_client.obtener_voluntario(code)
        if not existing or "error" in existing:
            raise NotFoundError("Voluntario no encontrado")
        if user.get("rut") != existing.get("rut"):
            raise AuthError("No tienes permiso para registrar horas de este voluntario")

    if not (1 <= body.horas <= 24):
        raise ValidationError("Las horas deben estar entre 1 y 24")

    data = {
        "horas": body.horas,
        "descripcion": body.descripcion,
        "registrado_por_rut": user.get("rut", ""),
        "centro_id": body.centro_id,
    }
    result = await voluntarios_client.registrar_horas(code, data)
    if "error" in result:
        raise ValidationError(result.get("error", "Error al registrar horas"))
    return RegistroHorasOut(
        id=str(result.get("id", "")),
        voluntario=str(result.get("voluntario", "")),
        centro_id=str(result.get("centro_id", "")),
        horas=result.get("horas", 0),
        descripcion=result.get("descripcion", ""),
        registrado_por_rut=result.get("registrado_por_rut", ""),
        fecha=str(result.get("fecha", "")),
    )


async def listar_horas(code: str, user: dict, uat: str = None, centro_id: str = None) -> HorasVoluntarioOut:
    data = await voluntarios_client.listar_horas(code, centro_id=centro_id)
    if "error" in data:
        raise NotFoundError("Voluntario no encontrado")
    return HorasVoluntarioOut(**data)


async def listar_centros(code: str, user: dict, uat: str = None) -> list[VoluntarioCentroOut]:
    centros = await voluntarios_client.listar_voluntario_centros(
        params={"voluntario_id": code}
    )
    return [VoluntarioCentroOut(**_centro_to_out(c)) for c in centros]


async def solicitar_centro(voluntario_id: str, centro_id: str, user: dict) -> VoluntarioCentroOut:
    try:
        centro = await logistica_client.obtener_centro(int(centro_id))
        if not centro or "error" in centro:
            raise ValidationError(f"El centro {centro_id} no existe en logística")
    except (ValueError, TypeError):
        raise ValidationError(f"El ID del centro '{centro_id}' no es válido")
    except ValidationError:
        raise
    except Exception:
        pass

    data = {
        "voluntario": int(voluntario_id),
        "centro_id": centro_id,
    }
    result = await voluntarios_client.crear_voluntario_centro(data)
    if not result or "error" in result:
        msg = result.get("error", "Error al solicitar centro") if isinstance(result, dict) else "Error al solicitar centro"
        if isinstance(result, dict) and result.get("status") == 409:
            raise ValidationError(f"Ya existe una solicitud para el centro {centro_id}")
        raise ValidationError(msg)
    return VoluntarioCentroOut(**_centro_to_out(result))


async def actualizar_centro(code: str, body, user: dict) -> VoluntarioCentroOut:
    if user.get("rol") not in ("admin", "encargado"):
        raise AuthError("Solo admin o encargado pueden actualizar asignaciones de centro")
    data = {"estado": body.estado}
    result = await voluntarios_client.actualizar_voluntario_centro(code, data)
    if not result or "error" in result:
        raise ValidationError("Error al actualizar asignación de centro")
    return VoluntarioCentroOut(**_centro_to_out(result))


async def eliminar_centro(code: str, user: dict) -> None:
    result = await voluntarios_client.eliminar_voluntario_centro(code)
    if result and "error" in result:
        raise ValidationError("Error al eliminar asignación de centro")


async def enviar_notificacion(body, user: dict) -> NotificacionOut:
    if user.get("rol") not in ("admin", "encargado"):
        raise AuthError("Solo admin o encargado pueden enviar notificaciones")
    data = {
        "voluntario_id": body.voluntario_id,
        "titulo": body.titulo,
        "mensaje": body.mensaje,
        "enviado_por_rut": user.get("rut", ""),
    }
    result = await voluntarios_client.crear_notificacion(data)
    if not result or "error" in result:
        raise ValidationError("Error al enviar notificación")
    return NotificacionOut(
        id=str(result.get("id", "")),
        voluntario=str(result.get("voluntario", "")),
        titulo=result.get("titulo", ""),
        mensaje=result.get("mensaje", ""),
        leida=result.get("leida", False),
        enviado_por_rut=result.get("enviado_por_rut", ""),
        fecha_creacion=str(result.get("fecha_creacion", "")),
    )


async def listar_notificaciones(voluntario_id: str) -> list[NotificacionOut]:
    items = await voluntarios_client.listar_notificaciones(
        params={"voluntario_id": voluntario_id}
    )
    return [
        NotificacionOut(
            id=str(n.get("id", "")),
            voluntario=str(n.get("voluntario", "")),
            titulo=n.get("titulo", ""),
            mensaje=n.get("mensaje", ""),
            leida=n.get("leida", False),
            enviado_por_rut=n.get("enviado_por_rut", ""),
            fecha_creacion=str(n.get("fecha_creacion", "")),
        )
        for n in items
    ]


async def marcar_notificacion_leida(notif_id: str) -> dict:
    result = await voluntarios_client.marcar_notificacion_leida(notif_id)
    if not result or "error" in result:
        raise ValidationError("Error al marcar notificación")
    return result


async def contar_asignados(necesidad_id: int) -> int:
    try:
        asignaciones = await voluntarios_client.listar_asignaciones(params={"necesidad_id": necesidad_id})
        return len(asignaciones)
    except Exception:
        return 0


async def inscribir_voluntario(voluntario_id: int, necesidad_id: int, user: dict) -> dict:
    from ..schemas.voluntarios import AsignacionVoluntarioOut

    rut = user.get("rut", "")
    if not rut:
        raise AuthError("Usuario no autenticado")

    existing = await voluntarios_client.listar_asignaciones(
        params={"necesidad_id": necesidad_id, "rut": rut}
    )
    if existing and len(existing) > 0:
        raise ValidationError("Ya estás inscrito en esta oportunidad de voluntariado")

    data = {
        "voluntario": voluntario_id,
        "necesidad_id": necesidad_id,
    }
    result = await voluntarios_client.crear_asignacion(data)
    if not result or "error" in result:
        raise ValidationError("Error al inscribirse en la oportunidad")
    return AsignacionVoluntarioOut(
        id=str(result.get("id", "")),
        voluntario=result.get("voluntario", voluntario_id),
        necesidad_id=result.get("necesidad_id", necesidad_id),
        estado=result.get("estado", "propuesto"),
        fecha_asignacion=str(result.get("fecha_asignacion", "")),
        fecha_actualizacion=str(result.get("fecha_actualizacion", "")),
    )
