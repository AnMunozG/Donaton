from ..schemas.donaciones import DonacionOut
from ..exceptions import NotFoundError
from ..clients.donaciones_client import DonacionesClient
from ..clients.logistica_client import LogisticaClient

donaciones_client = DonacionesClient()
logistica_client = LogisticaClient()


async def list_all(estado: str = None, centro_code: str = None, tipo: str = None) -> list[DonacionOut]:
    try:
        params = {}
        if estado: params["estado"] = estado
        if centro_code: params["centro_code"] = centro_code
        if tipo: params["tipo"] = tipo
        
        donaciones_data = await donaciones_client.listar_donaciones(params=params)
        return [DonacionOut(**d) for d in donaciones_data]
    except Exception:
        return []


async def get_by_code(code: str) -> DonacionOut:
    donacion_data = await donaciones_client.obtener_donacion(code)
    if not donacion_data:
        raise NotFoundError(f"No se encontró la donación con el código {code}")
    return DonacionOut(**donacion_data)


async def create(body, rut: str) -> DonacionOut:
    data = body.dict()
    data["origen"] = rut

    donacion_real_data = await donaciones_client.crear_donacion(data)
    
    if not donacion_real_data:
        raise NotFoundError("El microservicio de donaciones no procesó la solicitud.")

    if "error" in donacion_real_data:
        raise Exception(donacion_real_data.get("error", "Error del microservicio de donaciones"))

    tipo_recurso = donacion_real_data.get("tipo")
    cantidad_donada = int(donacion_real_data.get("cantidad", 0))
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
                        cantidad_actual = int(str(item["cantidad"]).split()[0].replace(".", ""))
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
                
                nuevo_estado = "Normal"
                if porcentaje >= 90:
                    nuevo_estado = "Capacidad crítica"
                elif porcentaje >= 70:
                    nuevo_estado = "Capacidad moderada"

                await logistica_client.actualizar_centro(int(centro_id), {
                    "inventario": inventario_actual,
                    "capacidadUsada": nueva_capacidad_usada,
                    "estado": nuevo_estado
                })
        except Exception as log_error:
            print(f"Alerta: Donación creada, pero falló actualización logística: {str(log_error)}")

    return DonacionOut(**donacion_real_data)


async def update_estado(code: str, nuevo_estado: str) -> DonacionOut:
    donacion_actualizada = await donaciones_client.actualizar_estado_donacion(code, {"estado": nuevo_estado})
    if not donacion_actualizada:
        raise NotFoundError(f"No se pudo actualizar la donación {code}")
    return DonacionOut(**donacion_actualizada)


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
