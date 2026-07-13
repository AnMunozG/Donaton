from datetime import datetime
from ..schemas.impacto import ImpactoOut, ImpactoPorMes, CentroImpactado
from ..clients import donaciones_client, logistica_client


async def get_impacto(rut: str) -> ImpactoOut:
    try:
        donaciones_data = await donaciones_client.listar_donaciones(params={"origen": rut})
    except Exception:
        donaciones_data = []

    if not isinstance(donaciones_data, list):
        donaciones_data = []

    total_donaciones = len(donaciones_data)
    total_kg = 0.0
    total_items = 0
    total_monetario = 0.0
    centros_set = set()
    por_tipo = {}
    por_mes = {}
    por_mes_kg = {}
    centros_dict = {}
    ultima_donacion = None

    for d in donaciones_data:
        items = d.get("items") or []
        tipo = d.get("tipo") or "Otros"
        centro_id = str(d.get("centroId", ""))
        fecha_str = d.get("fecha", "")

        if fecha_str and len(fecha_str) >= 7:
            if not ultima_donacion or fecha_str > ultima_donacion:
                ultima_donacion = fecha_str
            mes_key = fecha_str[:7]
            por_mes[mes_key] = por_mes.get(mes_key, 0) + 1

        if centro_id:
            centros_set.add(centro_id)
            if centro_id not in centros_dict:
                centros_dict[centro_id] = {
                    "id": centro_id,
                    "nombre": "",
                    "total_donaciones": 0,
                    "total_kg": 0,
                }

        if items:
            for it in items:
                it_tipo = it.get("tipo") or tipo
                it_cantidad = float(it.get("cantidad", 0) or 0)
                it_unidad = it.get("unidad", "")
                por_tipo[it_tipo] = por_tipo.get(it_tipo, 0) + 1
                if centro_id:
                    centros_dict[centro_id]["total_donaciones"] += 1
                if it_tipo == "Donación Monetaria" or it_unidad.lower() in ("clp", "usd"):
                    total_monetario += it_cantidad
                else:
                    total_kg += it_cantidad
                    total_items += 1
                    if centro_id in centros_dict:
                        centros_dict[centro_id]["total_kg"] += it_cantidad
                    if fecha_str and len(fecha_str) >= 7:
                        mes_key = fecha_str[:7]
                        por_mes_kg[mes_key] = por_mes_kg.get(mes_key, 0) + it_cantidad
        else:
            cantidad = float(d.get("cantidad", 0) or 0)
            unidad = d.get("unidad", "")
            por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
            if centro_id:
                centros_dict[centro_id]["total_donaciones"] += 1
            if tipo == "Donación Monetaria" or unidad.lower() in ("clp", "usd"):
                total_monetario += cantidad
            else:
                total_kg += cantidad
                total_items += 1
                if centro_id in centros_dict:
                    centros_dict[centro_id]["total_kg"] += cantidad
                if fecha_str and len(fecha_str) >= 7:
                    mes_key = fecha_str[:7]
                    por_mes_kg[mes_key] = por_mes_kg.get(mes_key, 0) + cantidad

    # Enrich centros with names and coordinates
    for c_id in list(centros_dict.keys()):
        try:
            id_num = int(c_id)
        except (ValueError, TypeError):
            centros_dict[c_id]["nombre"] = c_id
            continue
        try:
            centro = await logistica_client.obtener_centro(id_num)
            if centro:
                centros_dict[c_id]["nombre"] = centro.get("nombre", c_id)
                lat = centro.get("latitud") or (centro.get("coordenadas") or {}).get("lat", 0)
                lng = centro.get("longitud") or (centro.get("coordenadas") or {}).get("lng", 0)
                centros_dict[c_id]["lat"] = float(lat or 0)
                centros_dict[c_id]["lng"] = float(lng or 0)
                centros_dict[c_id]["region"] = centro.get("region", "")
        except Exception:
            centros_dict[c_id]["nombre"] = c_id

    centros_list = [
        CentroImpactado(**c) for c in sorted(
            centros_dict.values(), key=lambda x: x["total_donaciones"], reverse=True
        )
    ]

    meses_list = [
        ImpactoPorMes(mes=m, cantidad=c, total_kg=round(por_mes_kg.get(m, 0), 2))
        for m, c in sorted(por_mes.items())
    ]

    return ImpactoOut(
        total_donaciones=total_donaciones,
        total_kg=round(total_kg, 2),
        total_items=total_items,
        total_monetario=round(total_monetario, 2),
        centros_distintos=len(centros_set),
        por_tipo=por_tipo,
        por_mes=meses_list,
        centros=centros_list,
        ultima_donacion=ultima_donacion,
    )
