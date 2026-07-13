from ..schemas.donaciones import DonacionOut, DonacionMultiCreate
from ..exceptions import NotFoundError, BffError
from ..clients.donaciones_client import DonacionesClient
from ..clients.logistica_client import LogisticaClient
from . import centro_service

donaciones_client = DonacionesClient()
logistica_client = LogisticaClient()


def _enrich_donacion(d: dict) -> dict:
    d = dict(d)
    items = d.get("items") or []
    if not d.get("tipo") and items:
        tipos = [it.get("tipo") for it in items if it.get("tipo")]
        if len(set(tipos)) == 1:
            d["tipo"] = tipos[0]
            d["unidad"] = items[0].get("unidad") or d.get("unidad")
        elif tipos:
            d["tipo"] = "Multi-item"
        total_cant = sum(float(it.get("cantidad", 0) or 0) for it in items)
        if total_cant and not d.get("cantidad"):
            d["cantidad"] = str(int(total_cant)) if total_cant == int(total_cant) else str(total_cant)
    return d


async def list_all(estado: str = None, centro_code: str = None, tipo: str = None, origen: str = None, user=None) -> list[DonacionOut]:
    try:
        params = {}
        if isinstance(user, dict) and user.get("rol") == "encargado":
            params["centro_code"] = user.get("centro_acopio_id")
        if estado: params["estado"] = estado
        if centro_code: params["centro_code"] = centro_code
        if tipo: params["tipo"] = tipo
        if origen: params["origen"] = origen

        donaciones_data = await donaciones_client.listar_donaciones(params=params)
        results = []
        for d in donaciones_data:
            enriched = _enrich_donacion(d)
            centro_id = str(enriched.get("centroId", ""))
            if centro_id:
                try:
                    c = await centro_service.get_by_code(centro_id)
                    enriched["centro"] = c.nombre
                except Exception:
                    enriched["centro"] = centro_id
            results.append(DonacionOut(**enriched))
        return results
    except Exception:
        return []


async def get_by_code(code: str) -> DonacionOut:
    donacion_data = await donaciones_client.obtener_donacion(code)
    if not donacion_data:
        raise NotFoundError(f"No se encontró la donación con el código {code}")
    enriched = _enrich_donacion(donacion_data)
    centro_id = str(enriched.get("centroId", ""))
    if centro_id:
        try:
            c = await centro_service.get_by_code(centro_id)
            enriched["centro"] = c.nombre
        except Exception:
            enriched["centro"] = centro_id
    return DonacionOut(**enriched)


async def create(body, rut: str) -> DonacionOut:
    data = body.dict()
    data["origen"] = rut

    donacion_real_data = await donaciones_client.crear_donacion(data)
    
    if not donacion_real_data:
        raise NotFoundError("El microservicio de donaciones no procesó la solicitud.")

    if "error" in donacion_real_data:
        raise Exception(donacion_real_data.get("error", "Error del microservicio de donaciones"))

    tipo_recurso = donacion_real_data.get("tipo")
    cantidad_donada = int(float(donacion_real_data.get("cantidad") or 0))
    unidad_donada = donacion_real_data.get("unidad")
    centro_id = donacion_real_data.get("centroId")

    if tipo_recurso != "Donación Monetaria" and centro_id:
        try:
            centro_data = await logistica_client.obtener_centro(int(centro_id))
            
            if centro_data:
                inventario_actual = centro_data.get("inventario", []) or []
                capacidad_total = int(centro_data.get("capacidadTotal", 0))
                capacidad_usada_actual = int(centro_data.get("capacidadUsada", 0))

                encontrado = False
                for item in inventario_actual:
                    nombre_item = item.get("item") or item.get("tipo")
                    if nombre_item == tipo_recurso and item.get("unidad") == unidad_donada:
                        cantidad_actual = int(float(str(item["cantidad"]).split()[0].replace(".", "", 1)))
                        item["cantidad"] = str(cantidad_actual + cantidad_donada)
                        encontrado = True
                        break
                
                if not encontrado:
                    inventario_actual.append({
                        "tipo": tipo_recurso,
                        "cantidad": str(cantidad_donada),
                        "unidad": unidad_donada
                    })

                nueva_capacidad_usada = capacidad_usada_actual + cantidad_donada
                porcentaje = (nueva_capacidad_usada / capacidad_total) * 100 if capacidad_total > 0 else 0
                
                nuevo_estado = "Activo"
                if porcentaje >= 85:
                    nuevo_estado = "Capacidad crítica"

                await logistica_client.actualizar_centro(int(centro_id), {
                    "inventario": inventario_actual,
                    "capacidadUsada": nueva_capacidad_usada,
                    "estado": nuevo_estado
                })
        except Exception as log_error:
            print(f"Alerta: Donación creada, pero falló actualización logística: {str(log_error)}")

    enriched = _enrich_donacion(donacion_real_data)
    centro_id = str(enriched.get("centroId", ""))
    if centro_id:
        try:
            c = await centro_service.get_by_code(centro_id)
            enriched["centro"] = c.nombre
        except Exception:
            enriched["centro"] = centro_id
    return DonacionOut(**enriched)


async def create_multi(body: DonacionMultiCreate, rut: str) -> DonacionOut:
    data = body.dict()
    data["origen"] = rut
    items_data = data.pop("items", [])

    detalles = dict(data.pop("detalles", {}) or {})
    if data.get("notas"):
        detalles["notas"] = data.pop("notas")
    if data.get("direccion_retiro"):
        detalles["direccion_retiro"] = data.pop("direccion_retiro")
    if data.get("fecha_retiro"):
        detalles["fecha_retiro"] = data.pop("fecha_retiro")

    payload = {
        "origen": data["origen"],
        "centroId": data["centroId"],
        "fecha": data.get("fecha", ""),
        "estado": data.get("estado", "Donación Registrada"),
        "detalles": detalles,
        "items": [
            {
                "tipo": item["tipo"],
                "cantidad": item["cantidad"],
                "unidad": item["unidad"],
                "detalles": item.get("detalles", {}),
            }
            for item in items_data
        ],
    }

    donacion_real_data = await donaciones_client.crear_donacion_multi(payload)

    if not donacion_real_data:
        raise NotFoundError("El microservicio de donaciones no procesó la solicitud.")

    if "error" in donacion_real_data:
        raise Exception(donacion_real_data.get("error", "Error del microservicio de donaciones"))

    centro_id = donacion_real_data.get("centroId")

    tipos = [it["tipo"] for it in items_data if it.get("tipo")]
    total_cantidad = sum(float(it.get("cantidad", 0) or 0) for it in items_data)

    if tipos:
        update_padre = {}
        if len(set(tipos)) == 1:
            update_padre["tipo"] = tipos[0]
            update_padre["unidad"] = items_data[0].get("unidad", "")
        else:
            update_padre["tipo"] = "Multi-item"
        if total_cantidad:
            update_padre["cantidad"] = int(total_cantidad)
        if update_padre:
            try:
                await donaciones_client.actualizar_estado_donacion(
                    donacion_real_data.get("id", donacion_real_data.get("idDonacion", "")),
                    update_padre,
                )
                donacion_real_data.update(update_padre)
            except Exception:
                pass

    for item in items_data:
        tipo_recurso = item["tipo"]
        cantidad_donada = int(float(item.get("cantidad") or 0))
        unidad_donada = item["unidad"]

        if tipo_recurso != "Donación Monetaria" and centro_id:
            try:
                centro_data = await logistica_client.obtener_centro(int(centro_id))

                if centro_data:
                    inventario_actual = centro_data.get("inventario", []) or []
                    capacidad_total = int(centro_data.get("capacidadTotal", 0))
                    capacidad_usada_actual = int(centro_data.get("capacidadUsada", 0))

                    encontrado = False
                    for inv_item in inventario_actual:
                        nombre_item = inv_item.get("item") or inv_item.get("tipo")
                        if nombre_item == tipo_recurso and inv_item.get("unidad") == unidad_donada:
                            cantidad_actual = int(float(str(inv_item["cantidad"]).split()[0].replace(".", "", 1)))
                            inv_item["cantidad"] = str(cantidad_actual + cantidad_donada)
                            encontrado = True
                            break

                    if not encontrado:
                        inventario_actual.append({
                            "tipo": tipo_recurso,
                            "cantidad": str(cantidad_donada),
                            "unidad": unidad_donada,
                        })

                    nueva_capacidad_usada = capacidad_usada_actual + cantidad_donada
                    porcentaje = (nueva_capacidad_usada / capacidad_total) * 100 if capacidad_total > 0 else 0

                    nuevo_estado = "Activo"
                    if porcentaje >= 85:
                        nuevo_estado = "Capacidad crítica"

                    await logistica_client.actualizar_centro(int(centro_id), {
                        "inventario": inventario_actual,
                        "capacidadUsada": nueva_capacidad_usada,
                        "estado": nuevo_estado,
                    })
            except Exception as log_error:
                print(f"Alerta: Donación multi-item creada, pero falló actualización logística para {tipo_recurso}: {str(log_error)}")

    enriched = _enrich_donacion(donacion_real_data)
    centro_id = str(enriched.get("centroId", ""))
    if centro_id:
        try:
            c = await centro_service.get_by_code(centro_id)
            enriched["centro"] = c.nombre
        except Exception:
            enriched["centro"] = centro_id
    return DonacionOut(**enriched)


async def update_estado(code: str, nuevo_estado: str, user=None) -> DonacionOut:
    if isinstance(user, dict) and user.get("rol") == "encargado":
        donacion_data = await donaciones_client.obtener_donacion(code)
        if donacion_data and str(donacion_data.get("centroId")) != str(user.get("centro_acopio_id")):
            raise BffError("No tienes permiso para actualizar donaciones de este centro", status=403)
    donacion_actualizada = await donaciones_client.actualizar_estado_donacion(code, {"estado": nuevo_estado})
    if not donacion_actualizada:
        raise NotFoundError(f"No se pudo actualizar la donación {code}")
    return DonacionOut(**_enrich_donacion(donacion_actualizada))


async def delete(code: str) -> None:
    await donaciones_client.eliminar_donacion(code)


async def get_stats() -> dict:
    try:
        return await donaciones_client.obtener_estadisticas()
    except Exception:
        return {
            "total_donaciones": 0,
            "total_monto": 0,
            "total_beneficiarios": 0,
            "centros_activos": 0,
            "por_estado": {},
            "por_tipo": {},
        }
