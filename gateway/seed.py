"""
Script para poblar la base de datos con datos iniciales.
Uso: python manage.py shell < gateway/seed.py
"""
import os
import sys
import django
from datetime import date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from gateway.models import (
    Cuenta, Centro, TipoRecurso, Unidad, UnidadPorTipo,
    Equipo, Gobernanza, Hito, Valor, Reporte,
    Donacion, Necesidad, Propuesta, Envio,
)
from django.contrib.auth.hashers import make_password


def seed():
    print("Poblando base de datos...")

    # ── Cuentas ──
    cuentas_data = [
        {"rut": "111111111", "nombre": "Admin Donatón", "email": "admin@donaton.cl", "rol": "admin", "password": "admin1234"},
        {"rut": "222222222", "nombre": "Usuario Ejemplo", "email": "usuario@donaton.cl", "rol": "donante", "password": "user1234"},
        {"rut": "11.111.111-1", "nombre": "Admin Donatón", "email": "admin2@donaton.cl", "rol": "admin", "password": "admin123"},
        {"rut": "22.222.222-2", "nombre": "María García", "email": "maria@mail.cl", "rol": "donante", "password": "pass123"},
        {"rut": "33.333.333-3", "nombre": "Juan Pérez", "email": "juan@mail.cl", "rol": "beneficiario", "password": "pass123"},
        {"rut": "44.444.444-4", "nombre": "Centro Esperanza", "email": "esperanza@mail.cl", "rol": "beneficiario", "password": "pass123"},
        {"rut": "55.555.555-5", "nombre": "Voluntario Pedro", "email": "pedro@mail.cl", "rol": "voluntario", "password": "pass123"},
    ]
    for data in cuentas_data:
        obj, created = Cuenta.objects.get_or_create(
            rut=data["rut"],
            defaults={
                "nombre": data["nombre"],
                "email": data["email"],
                "rol": data["rol"],
                "password": make_password(data["password"]),
            },
        )
        if created:
            print(f"  Cuenta creada: {obj.nombre} ({obj.rut})")

    # ── Centros ──
    admin_cuenta = Cuenta.objects.filter(rol="admin").first()

    centros_data = [
        {"code": "CA-001", "nombre": "Centro de Acopio Santiago Centro", "region": "Metropolitana", "direccion": "Av. Libertador Bernardo O'Higgins 1234, Santiago", "telefono": "+56 9 8765 4321", "coordenadas_lat": -33.4489, "coordenadas_lng": -70.6693, "capacidad": 5000, "estado": "Activo", "inventario": [{"tipo": "Alimentos", "cantidad": "1.200 kg"}, {"tipo": "Ropa y abrigo", "cantidad": "8 cajas"}, {"tipo": "Insumos médicos", "cantidad": "45 unidades"}]},
        {"code": "CA-002", "nombre": "Centro de Acopio Puente Alto", "region": "Metropolitana", "direccion": "Calle Los Quillayes 456, Puente Alto", "telefono": "+56 9 7654 3210", "coordenadas_lat": -33.5929, "coordenadas_lng": -70.5759, "capacidad": 3000, "estado": "Capacidad crítica", "inventario": [{"tipo": "Alimentos", "cantidad": "900 kg"}, {"tipo": "Artículos de higiene", "cantidad": "120 unidades"}]},
        {"code": "CA-003", "nombre": "Centro de Acopio Maipú", "region": "Metropolitana", "direccion": "Av. Pajaritos 789, Maipú", "telefono": "+56 9 6543 2109", "coordenadas_lat": -33.5113, "coordenadas_lng": -70.7567, "capacidad": 4000, "estado": "Activo", "inventario": [{"tipo": "Ropa y abrigo", "cantidad": "15 cajas"}, {"tipo": "Utensilios del hogar", "cantidad": "30 unidades"}]},
        {"code": "CA-004", "nombre": "Centro de Acopio Valparaíso", "region": "Valparaíso", "direccion": "Av. Argentina 321, Valparaíso", "telefono": "+56 9 5432 1098", "coordenadas_lat": -33.0458, "coordenadas_lng": -71.6197, "capacidad": 3500, "estado": "Activo", "inventario": [{"tipo": "Alimentos", "cantidad": "300 kg"}, {"tipo": "Insumos médicos", "cantidad": "18 unidades"}]},
        {"code": "CA-005", "nombre": "Centro de Acopio Concepción", "region": "Biobío", "direccion": "Av. Costanera 555, Concepción", "telefono": "+56 9 4321 0987", "coordenadas_lat": -36.8270, "coordenadas_lng": -73.0503, "capacidad": 4500, "estado": "Activo", "inventario": [{"tipo": "Alimentos", "cantidad": "600 kg"}, {"tipo": "Pañales e infantiles", "cantidad": "200 unidades"}]},
        {"code": "CA-006", "nombre": "Centro de Acopio La Serena", "region": "Coquimbo", "direccion": "Av. Juan Bohón 888, La Serena", "telefono": "+56 9 3210 9876", "coordenadas_lat": -29.9027, "coordenadas_lng": -71.2520, "capacidad": 3000, "estado": "Activo", "inventario": [{"tipo": "Alimentos", "cantidad": "750 kg"}, {"tipo": "Ropa y abrigo", "cantidad": "12 cajas"}, {"tipo": "Artículos de higiene", "cantidad": "80 kits"}]},
    ]
    for data in centros_data:
        obj, created = Centro.objects.get_or_create(
            code=data["code"],
            defaults={
                "nombre": data["nombre"],
                "region": data["region"],
                "direccion": data["direccion"],
                "telefono": data["telefono"],
                "coordenadas_lat": data["coordenadas_lat"],
                "coordenadas_lng": data["coordenadas_lng"],
                "capacidad": data["capacidad"],
                "estado": data["estado"],
                "inventario": data["inventario"],
                "encargado": admin_cuenta,
            },
        )
        if created:
            print(f"  Centro creado: {obj.nombre} ({obj.code})")

    # ── Tipos de Recurso ──
    tipos_data = [
        {"code": "TR-001", "nombre": "Alimentos no perecibles", "descripcion": "Arroz, fideos, legumbres, conservas, etc."},
        {"code": "TR-002", "nombre": "Ropa y abrigo", "descripcion": "Ropa en buen estado para todas las edades"},
        {"code": "TR-003", "nombre": "Artículos de higiene", "descripcion": "Jabón, shampoo, pasta dental, papel higiénico"},
        {"code": "TR-004", "nombre": "Insumos médicos", "descripcion": "Medicamentos sin receta y kits de primeros auxilios"},
        {"code": "TR-005", "nombre": "Útiles escolares", "descripcion": "Cuadernos, lápices, mochilas, libros"},
        {"code": "TR-006", "nombre": "Utensilios del hogar", "descripcion": "Ollas, platos, cubiertos y elementos básicos"},
        {"code": "TR-007", "nombre": "Donación Monetaria", "descripcion": "Donaciones en dinero"},
    ]
    for data in tipos_data:
        obj, created = TipoRecurso.objects.get_or_create(
            code=data["code"],
            defaults={"nombre": data["nombre"], "descripcion": data["descripcion"]},
        )
        if created:
            print(f"  Tipo recurso creado: {obj.nombre}")

    # ── Unidades ──
    unidades_data = [
        {"code": "UN-001", "nombre": "kg", "abreviatura": "kg"},
        {"code": "UN-002", "nombre": "unidades", "abreviatura": "unid."},
        {"code": "UN-003", "nombre": "cajas", "abreviatura": "caja"},
        {"code": "UN-004", "nombre": "kits", "abreviatura": "kit"},
        {"code": "UN-005", "nombre": "prendas", "abreviatura": "prenda"},
        {"code": "UN-006", "nombre": "CLP", "abreviatura": "$"},
        {"code": "UN-007", "nombre": "USD", "abreviatura": "USD"},
        {"code": "UN-008", "nombre": "juegos", "abreviatura": "juego"},
        {"code": "UN-009", "nombre": "L", "abreviatura": "L"},
        {"code": "UN-010", "nombre": "sobres", "abreviatura": "sobre"},
    ]
    for data in unidades_data:
        obj, created = Unidad.objects.get_or_create(
            code=data["code"],
            defaults={"nombre": data["nombre"], "abreviatura": data["abreviatura"]},
        )
        if created:
            print(f"  Unidad creada: {obj.nombre} ({obj.abreviatura})")

    # ── Unidades por Tipo ──
    unidades_por_tipo = {
        "Alimentos no perecibles": ["kg", "unidades", "cajas"],
        "Insumos médicos": ["unidades", "cajas", "sobres"],
        "Artículos de higiene": ["unidades", "kits", "cajas"],
        "Ropa y abrigo": ["prendas", "cajas", "kits"],
        "Donación Monetaria": ["CLP", "USD"],
        "Utensilios del hogar": ["unidades", "juegos", "cajas"],
    }
    for tipo_nombre, unidad_nombres in unidades_por_tipo.items():
        tr = TipoRecurso.objects.filter(nombre=tipo_nombre).first()
        if not tr:
            continue
        for u_nombre in unidad_nombres:
            un = Unidad.objects.filter(nombre=u_nombre).first()
            if un:
                UnidadPorTipo.objects.get_or_create(tipo_recurso=tr, unidad=un)

    # ── Donaciones ──
    donaciones_data = [
        {"code": "DO-001", "tipo": "Alimentos no perecibles", "cantidad": 50, "unidad": "kg", "origen": "Empresa Sodimac", "centro": "CA-001", "fecha": "2026-04-01", "estado": "Entregado", "detalles": {"marca": "Marca Propia", "fechaVencimiento": "2027-12-31", "tipoAlimento": "Granos y legumbres", "pesoUnitario": "1 kg", "condicionesAlmacenamiento": "Lugar seco y fresco"}},
        {"code": "DO-011", "tipo": "Ropa y abrigo", "cantidad": 30, "unidad": "prendas", "origen": "Voluntarios Recoleta", "centro": "CA-006", "fecha": "2026-04-15", "estado": "En acopio", "detalles": {"categoria": "Abrigo", "tallas": ["Única"], "genero": "Unisex", "estadoPrenda": "Usada en buen estado", "material": "Algodón"}},
        {"code": "DO-012", "tipo": "Alimentos no perecibles", "cantidad": 10, "unidad": "kg", "origen": "222222222", "centro": "CA-001", "fecha": "2026-05-01", "estado": "En acopio", "detalles": {"tipoAlimento": "Granos y legumbres", "fechaVencimiento": "2027-12-31", "condicionesAlmacenamiento": "Lugar seco", "tipoEnvase": "Bolsa sellada"}},
        {"code": "DO-013", "tipo": "Artículos de higiene", "cantidad": 5, "unidad": "kits", "origen": "222222222", "centro": "CA-002", "fecha": "2026-04-28", "estado": "Entregado", "detalles": {"tipoKit": "Higiene personal básico", "contenido": ["Jabón", "Shampoo", "Pasta dental"], "destinatario": "Adultos mayores", "marca": "Varias"}},
        {"code": "DO-014", "tipo": "Donación Monetaria", "cantidad": 50000, "unidad": "CLP", "origen": "222222222", "centro": "CA-001", "fecha": "2026-04-20", "estado": "Entregado", "detalles": {}},
    ]
    for d in donaciones_data:
        _, created = Donacion.objects.get_or_create(
            code=d["code"],
            defaults={
                "tipo": d["tipo"],
                "cantidad": d["cantidad"],
                "unidad": Unidad.objects.get(nombre=d["unidad"]),
                "origen_display": d["origen"],
                "centro": Centro.objects.get(code=d["centro"]),
                "fecha": date.fromisoformat(d["fecha"]),
                "estado": d["estado"],
                "detalles": d["detalles"],
            },
        )
        if created:
            print(f"  Donación creada: {d['code']}")

    # ── Necesidades ──
    necesidades_data = [
        {"code": "NE-001", "recurso": "Alimentos no perecibles", "cantidad": 15, "donado": 13, "unidad": "kg", "urgencia": "Alta", "estado": "Asignado", "centro": "CA-001", "reportadoPor": "Municipalidad de Santiago Centro", "detalles": {"tipoAlimento": "Granos, legumbres y aceite", "beneficiarios": "Familias damnificadas por incendios", "fechaEstimadaEntrega": "2026-04-10"}},
        {"code": "NE-002", "recurso": "Ropa y abrigo", "cantidad": 15, "donado": 5, "unidad": "prendas", "urgencia": "Media", "estado": "Asignado", "centro": "CA-002", "reportadoPor": "Voluntario en terreno", "detalles": {"tallasNecesarias": ["S", "M", "L", "XL"], "tipoPrenda": "Frazadas y parkas", "beneficiarios": "Personas mayores en albergue", "temporada": "Invierno"}},
        {"code": "NE-003", "recurso": "Insumos médicos", "cantidad": 30, "donado": 25, "unidad": "unidades", "urgencia": "Alta", "estado": "Pendiente", "centro": "CA-004", "reportadoPor": "Centro médico local", "detalles": {"tipoMedicamento": "Analgésicos, antibióticos y antipiréticos", "restricciones": "No vencidos, cajas cerradas", "beneficiarios": "Familias del campamento"}},
        {"code": "NE-004", "recurso": "Artículos de higiene", "cantidad": 20, "donado": 20, "unidad": "kits", "urgencia": "Baja", "estado": "Cubierto", "centro": "CA-004", "reportadoPor": "Voluntario en terreno", "detalles": {"contenidoKit": ["Jabón", "Shampoo", "Pasta dental", "Toallas húmedas"], "destinatario": "Niños y adultos mayores", "frecuencia": "Entrega única"}},
        {"code": "NE-005", "recurso": "Alimentos no perecibles", "cantidad": 20, "donado": 3, "unidad": "kg", "urgencia": "Alta", "estado": "Asignado", "centro": "CA-001", "reportadoPor": "Junta de vecinos", "detalles": {"tipoAlimento": "Leche en polvo, enlatados y cereales", "beneficiarios": "Familias con niños pequeños", "fechaEstimadaEntrega": "2026-04-12"}},
    ]
    for n in necesidades_data:
        _, created = Necesidad.objects.get_or_create(
            code=n["code"],
            defaults={
                "centro": Centro.objects.get(code=n["centro"]),
                "tipo_recurso": TipoRecurso.objects.get(nombre=n["recurso"]),
                "cantidad_requerida": n["cantidad"],
                "cantidad_recibida": n["donado"],
                "unidad": Unidad.objects.get(nombre=n["unidad"]),
                "urgencia": n["urgencia"],
                "estado": n["estado"],
                "reportado_por": n["reportadoPor"],
                "detalles": n["detalles"],
                "creada_por": admin_cuenta,
            },
        )
        if created:
            print(f"  Necesidad creada: {n['code']}")

    # ── Envíos ──
    envios_data = [
        {"code": "EN-001", "donacion": "DO-001", "centro": "CA-001", "destino": "Sector Las Rosas, Concepción", "fecha_salida": "2026-04-02", "fecha_entrega": "2026-04-03", "estado": "Entregado", "transportista": "Flota Donatón Norte"},
        {"code": "EN-002", "donacion": None, "centro": "CA-003", "destino": "Albergue Municipal, Talca", "fecha_salida": "2026-04-04", "fecha_entrega": None, "estado": "En tránsito", "transportista": "Flota Donatón Sur"},
        {"code": "EN-003", "donacion": None, "centro": "CA-002", "destino": "Campamento El Pino, Valparaíso", "fecha_salida": None, "fecha_entrega": None, "estado": "Pendiente despacho", "transportista": ""},
    ]
    for e in envios_data:
        donacion = None
        if e["donacion"]:
            try:
                donacion = Donacion.objects.get(code=e["donacion"])
            except Donacion.DoesNotExist:
                pass
        fecha_salida = date.fromisoformat(e["fecha_salida"]) if e["fecha_salida"] else None
        fecha_entrega = date.fromisoformat(e["fecha_entrega"]) if e["fecha_entrega"] else None
        _, created = Envio.objects.get_or_create(
            code=e["code"],
            defaults={
                "donacion": donacion,
                "centro": Centro.objects.get(code=e["centro"]),
                "destino": e["destino"],
                "fecha_salida": fecha_salida,
                "fecha_entrega": fecha_entrega,
                "estado": e["estado"],
                "transportista": e["transportista"],
            },
        )
        if created:
            print(f"  Envío creado: {e['code']}")

    # ── Equipo ──
    equipo_data = [
        {"nombre": "Angel Exzequiel Muñoz González", "cargo": "Desarrollador Frontend", "email": "angel@donaton.cl", "foto_url": "", "activo": True},
        {"nombre": "Yasser Antonio Yamil Illanes", "cargo": "Desarrollador Backend", "email": "yasser@donaton.cl", "foto_url": "", "activo": True},
        {"nombre": "Martin Ignacio Pizarro Estay", "cargo": "Desarrollador Backend", "email": "martin@donaton.cl", "foto_url": "", "activo": True},
    ]
    for data in equipo_data:
        obj, created = Equipo.objects.get_or_create(
            nombre=data["nombre"],
            defaults={"cargo": data["cargo"], "email": data["email"], "foto_url": data["foto_url"], "activo": data["activo"]},
        )
        if created:
            print(f"  Miembro equipo creado: {obj.nombre}")

    # ── Gobernanza ──
    gobernanza_data = [
        {"nombre": "Angel Exzequiel Muñoz González", "cargo": "Lider Corporativo", "img_url": "https://i.imgflip.com/9e4vwk.jpg"},
        {"nombre": "Yasser Antonio Yamil Illanes", "cargo": "Lider de Operaciones y Logistica", "img_url": "https://i.ytimg.com/vi/amp6D_XRH3I/hq720.jpg"},
        {"nombre": "Martin Ignacio Pizarro Estay", "cargo": "Lider de Relaciones Públicas", "img_url": "https://media.tenor.com/ThwiQuVpaicAAAAM/cat-licking-a-lollipop-and-being-super-cool.gif"},
    ]
    for data in gobernanza_data:
        obj, created = Gobernanza.objects.get_or_create(
            nombre=data["nombre"],
            defaults={"cargo": data["cargo"], "img_url": data["img_url"]},
        )
        if created:
            print(f"  Gobernanza creada: {obj.nombre}")

    # ── Hitos ──
    hitos_data = [
        {"year": "2023", "titulo": "Fundación de Donatón", "descripcion": "Nace como proyecto universitario para resolver el caos logístico en emergencias.", "tipo": "logro"},
        {"year": "2024", "titulo": "Primeros centros activos", "descripcion": "Integramos 12 centros de acopio en la Región Metropolitana con trazabilidad completa.", "tipo": "logro"},
        {"year": "2025", "titulo": "Expansión nacional", "descripcion": "Llegamos a 38 centros activos en 6 regiones del país, con más de 5.200 familias beneficiadas.", "tipo": "logro"},
        {"year": "2026", "titulo": "Plataforma integral", "descripcion": "Lanzamos back-office, transparencia pública y reportes en tiempo real para toda la comunidad.", "tipo": "logro"},
    ]
    for data in hitos_data:
        obj, created = Hito.objects.get_or_create(
            titulo=data["titulo"],
            defaults={"year": data["year"], "descripcion": data["descripcion"], "tipo": data["tipo"]},
        )
        if created:
            print(f"  Hito creado: {obj.titulo}")

    # ── Valores ──
    valores_data = [
        {"titulo": "Transparencia", "descripcion": "Cada donación es rastreable desde el origen hasta su entrega. Nadie queda en la oscuridad.", "icono": "bi-transparency"},
        {"titulo": "Seguridad", "descripcion": "Protegemos los datos de donantes y beneficiarios con autenticación centralizada y acceso controlado.", "icono": "bi-shield-check"},
        {"titulo": "Sostenibilidad", "descripcion": "Nuestra arquitectura modular permite crecer sin comprometer la operación actual de la organización.", "icono": "bi-arrow-repeat"},
        {"titulo": "Coordinación", "descripcion": "Conectamos donantes, empresas, municipalidades y equipos logísticos en un único sistema integrado.", "icono": "bi-people-fill"},
    ]
    for data in valores_data:
        obj, created = Valor.objects.get_or_create(
            titulo=data["titulo"],
            defaults={"descripcion": data["descripcion"], "icono": data["icono"]},
        )
        if created:
            print(f"  Valor creado: {obj.titulo}")

    # ── Reportes ──
    reportes_data = [
        {"titulo": "Reporte Anual 2025", "fecha": "2026-01-15", "tipo": "PDF", "size": "2.4 MB", "icono": "bi-file-earmark-pdf-fill", "color": "#DD4444"},
        {"titulo": "Estado Financiero Q4 2025", "fecha": "2025-12-01", "tipo": "PDF", "size": "1.8 MB", "icono": "bi-file-earmark-pdf-fill", "color": "#DD4444"},
        {"titulo": "Balance Social 2025", "fecha": "2025-11-15", "tipo": "PDF", "size": "3.1 MB", "icono": "bi-file-earmark-pdf-fill", "color": "#DD4444"},
        {"titulo": "Auditoría Externa 2025", "fecha": "2025-10-01", "tipo": "PDF", "size": "4.2 MB", "icono": "bi-file-earmark-check-fill", "color": "#3AB795"},
        {"titulo": "Informe de Impacto por Región", "fecha": "2025-09-15", "tipo": "XLSX", "size": "1.2 MB", "icono": "bi-file-earmark-spreadsheet-fill", "color": "#194B4F"},
        {"titulo": "Memoria de Gestión 2024-2025", "fecha": "2025-08-01", "tipo": "PDF", "size": "5.7 MB", "icono": "bi-file-earmark-text-fill", "color": "#F48080"},
    ]
    for data in reportes_data:
        obj, created = Reporte.objects.get_or_create(
            titulo=data["titulo"],
            defaults={
                "fecha": date.fromisoformat(data["fecha"]),
                "tipo": data["tipo"],
                "size": data["size"],
                "icono": data["icono"],
                "color": data["color"],
            },
        )
        if created:
            print(f"  Reporte creado: {obj.titulo}")

    print("¡Base de datos poblada exitosamente!")


if __name__ == "__main__":
    seed()
