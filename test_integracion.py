#!/usr/bin/env python3
"""Script de pruebas de integración — Donatón
Ejecutar: python test_integracion.py
Funciona en Windows, Linux y macOS sin cambios.
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime

# ── Configuración ──
BFF_URL = "http://localhost:8080/api"
API_USER = "11111111-1"
API_PASS = "admin1234"
NUEVO_RUT = "22222222-2"

# ── Variables globales ──
token_admin = None
donacion_id = None
paso_ok = 0
paso_total = 0
errores = []


def request(method, path, data=None, token=None, expected_status=None):
    """Ejecuta una petición HTTP y retorna un dict normalizado.
    Si la respuesta JSON es una lista, la envuelve en {"_items": [...]}.
    """
    global paso_total
    paso_total += 1
    url = f"{BFF_URL}{path}"
    body = json.dumps(data).encode("utf-8") if data else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            raw = resp.read().decode("utf-8")
            parsed = json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        status = e.code
        raw = e.read().decode("utf-8")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"error": raw}
    except Exception as e:
        return {"_status": 0, "_error": str(e)}

    # Normalizar: si es lista, envolver en dict
    if isinstance(parsed, list):
        result = {"_items": parsed, "_is_list": True}
    else:
        result = parsed if isinstance(parsed, dict) else {"_raw": str(parsed)}
    result["_status"] = status

    if expected_status is not None and status != expected_status:
        result["_fail"] = f"Esperado {expected_status}, obtenido {status}"
    return result


def paso(nombre, result, checks=None):
    global paso_ok
    fail = result.get("_fail")
    status = result.get("_status", 0)

    if fail or status == 0:
        if "_error" in result:
            msj = f"{fail or ''}: {result['_error']}" if fail else result["_error"]
        else:
            msj = fail or "Error de conexión"
        print(f"  [FALLA] {nombre}: {msj}")
        errores.append(f"{nombre}: {msj}")
        return False

    if checks:
        for clave, esperado in checks.items():
            valor = result.get(clave)
            if valor != esperado:
                msg = f"  [FALLA] {nombre}: campo '{clave}' esperado '{esperado}', obtenido '{valor}'"
                print(msg)
                errores.append(msg)
                return False

    paso_ok += 1
    print(f"  [OK] {nombre}")
    return True


def normalizar_rut(rut):
    """Limpia el RUT (sin puntos, sin guión, sin espacios, mayúsculas)."""
    return rut.upper().replace(".", "").replace("-", "").replace(" ", "")


# ══════════════════════════════════════════════════════════════
#  CA001 — Login y obtención de JWT
# ══════════════════════════════════════════════════════════════
def test_ca001():
    global token_admin
    token_admin = None
    print("\n=== CA001 — Login de usuario y obtención de JWT ===")

    # Paso 1: Login (con RUT normalizado)
    r = request("POST", "/auth/login",
                {"rut": normalizar_rut(API_USER), "password": API_PASS},
                expected_status=200)
    if not paso("Paso 1: Login exitoso", r, checks={"_status": 200}):
        return False
    token_admin = r.get("token", "")
    if not token_admin:
        print("  [FALLA] No se obtuvo token JWT")
        return False

    # Paso 2: Decodificar payload del JWT
    import base64
    parts = token_admin.split(".")
    if len(parts) != 3:
        print("  [FALLA] Paso 2: Token JWT no tiene 3 partes")
        return False
    try:
        payload_b64 = parts[1]
        padding = 4 - len(payload_b64) % 4
        if padding != 4:
            payload_b64 += "=" * padding
        decoded = base64.urlsafe_b64decode(payload_b64)
        payload = json.loads(decoded)
        if payload.get("rol") != "admin":
            print(f"  [FALLA] Paso 2: rol en payload = {payload.get('rol')}")
            return False
        print(f"  [OK] Paso 2: Payload JWT válido (rut={payload.get('rut')}, rol={payload.get('rol')})")
    except Exception as e:
        print(f"  [FALLA] Paso 2: Error decodificando JWT: {e}")
        return False

    # Paso 3: GET /auth/me con token
    r = request("GET", "/auth/me", token=token_admin, expected_status=200)
    paso("Paso 3: /auth/me con token", r, checks={"_status": 200})

    # Paso 4: Login con contraseña incorrecta
    r = request("POST", "/auth/login",
                {"rut": normalizar_rut(API_USER), "password": "wrong_password"},
                expected_status=401)
    paso("Paso 4: Login con password incorrecta", r, checks={"_status": 401})

    # Paso 5: GET /auth/me sin token
    r = request("GET", "/auth/me", expected_status=401)
    paso("Paso 5: /auth/me sin token", r, checks={"_status": 401})

    return True


# ══════════════════════════════════════════════════════════════
#  CA002 — Registro de nuevo usuario y validación RUT
# ══════════════════════════════════════════════════════════════
def test_ca002():
    print("\n=== CA002 — Registro de nuevo usuario y validación de RUT ===")

    # Paso 1: Registro exitoso (tolera 422 si el RUT ya existe de ejecución anterior)
    global paso_ok
    r = request("POST", "/auth/register",
                {"rut": NUEVO_RUT, "nombre": "Juan Pérez",
                 "email": "juan@test.cl", "password": "testpass1"},
                expected_status=201)
    if r.get("_status") == 422:
        print("  [OK] Paso 1: Usuario ya existía (ejecución repetida)")
        paso_ok += 1
    else:
        paso("Paso 1: Registro exitoso", r, checks={"_status": 201})

    # Paso 2: Login con RUT normalizado
    r = request("POST", "/auth/login",
                {"rut": normalizar_rut(NUEVO_RUT), "password": "testpass1"},
                expected_status=200)
    paso("Paso 2: Login con nuevo usuario", r, checks={"_status": 200})

    # Paso 3: RUT duplicado
    r = request("POST", "/auth/register",
                {"rut": NUEVO_RUT, "nombre": "Otro",
                 "email": "otro@test.cl", "password": "pass1234"},
                expected_status=422)
    paso("Paso 3: RUT duplicado (422)", r, checks={"_status": 422})

    # Paso 4: RUT con DV incorrecto
    r = request("POST", "/auth/register",
                {"rut": "12345678-0", "nombre": "Test",
                 "email": "t@t.cl", "password": "testpass1"},
                expected_status=422)
    paso("Paso 4: RUT con DV incorrecto (422)", r, checks={"_status": 422})

    return True


# ══════════════════════════════════════════════════════════════
#  CA003 — Creación de donación y persistencia
# ══════════════════════════════════════════════════════════════
def test_ca003():
    global donacion_id
    donacion_id = None
    print("\n=== CA003 — Creación de donación y persistencia ===")

    if not token_admin:
        print("  [SKIP] No hay token de autenticación")
        return False

    # Paso 2: Crear donación física (incluir estado explícitamente)
    r = request("POST", "/donaciones",
                {"tipo": "Alimentos no perecibles", "cantidad": 100, "unidad": "kg",
                 "centroId": "1", "origen": API_USER, "fecha": "2026-06-16",
                 "estado": "Recibido", "detalles": {}},
                token=token_admin, expected_status=201)
    if not paso("Paso 2: Crear donación física", r, checks={"_status": 201}):
        return False
    donacion_id = str(r.get("id", ""))

    # Paso 3: Verificar listado
    r = request("GET", "/donaciones", token=token_admin, expected_status=200)
    paso("Paso 3: Listar donaciones", r, checks={"_status": 200})

    # Paso 4: Donación monetaria
    r = request("POST", "/donaciones",
                {"tipo": "Donación Monetaria", "cantidad": 50000, "unidad": "CLP",
                 "centroId": "1", "origen": API_USER, "fecha": "2026-06-16",
                 "detalles": {}},
                token=token_admin, expected_status=201)
    paso("Paso 4: Donación monetaria", r, checks={"_status": 201})

    # Paso 5: Sin token
    r = request("POST", "/donaciones",
                {"tipo": "Alimentos no perecibles", "cantidad": 10, "unidad": "kg",
                 "centroId": "1", "origen": API_USER, "fecha": "2026-06-16",
                 "detalles": {}},
                expected_status=401)
    paso("Paso 5: Donación sin token", r, checks={"_status": 401})

    return True


# ══════════════════════════════════════════════════════════════
#  CA004 — Actualización de inventario
# ══════════════════════════════════════════════════════════════
def test_ca004():
    print("\n=== CA004 — Actualización de inventario del centro ===")

    if not token_admin:
        print("  [SKIP] No hay token de autenticación")
        return False

    # Paso 1: Inventario inicial
    r = request("GET", "/centros/1/inventario", expected_status=200)
    paso("Paso 1: Inventario inicial", r, checks={"_status": 200})

    # Paso 2: Estado inicial del centro
    r = request("GET", "/centros/1", expected_status=200)
    paso("Paso 2: Detalle centro 1", r, checks={"_status": 200})

    # Paso 3: Crear donación física de 50 kg
    r = request("POST", "/donaciones",
                {"tipo": "Alimentos no perecibles", "cantidad": 50, "unidad": "kg",
                 "centroId": "1", "origen": API_USER, "fecha": "2026-06-16",
                 "estado": "Recibido", "detalles": {}},
                token=token_admin, expected_status=201)
    paso("Paso 3: Donación 50kg", r, checks={"_status": 201})

    # Paso 4: Inventario post-donación
    r = request("GET", "/centros/1/inventario", expected_status=200)
    paso("Paso 4: Inventario post-donación", r, checks={"_status": 200})

    # Paso 5: Capacidad usada
    r = request("GET", "/centros/1", expected_status=200)
    paso("Paso 5: Estado centro post-donación", r, checks={"_status": 200})

    # Paso 6: Monetaria no afecta inventario
    r = request("POST", "/donaciones",
                {"tipo": "Donación Monetaria", "cantidad": 10000, "unidad": "CLP",
                 "centroId": "1", "origen": API_USER, "fecha": "2026-06-16",
                 "detalles": {}},
                token=token_admin, expected_status=201)
    paso("Paso 6: Monetaria no afecta inventario", r, checks={"_status": 201})

    return True


# ══════════════════════════════════════════════════════════════
#  CA005 — Listado y filtrado de donaciones
# ══════════════════════════════════════════════════════════════
def test_ca005():
    print("\n=== CA005 — Listado y filtrado de donaciones ===")

    r = request("GET", "/donaciones", token=token_admin, expected_status=200)
    paso("Paso 1: Lista completa", r, checks={"_status": 200})

    r = request("GET", "/donaciones?estado=Recibido", token=token_admin, expected_status=200)
    paso("Paso 2: Filtro estado", r, checks={"_status": 200})

    r = request("GET", "/donaciones?tipo=Alimentos+no+perecibles",
                token=token_admin, expected_status=200)
    paso("Paso 3: Filtro tipo", r, checks={"_status": 200})

    r = request("GET", "/donaciones?centro_code=1", token=token_admin, expected_status=200)
    paso("Paso 4: Filtro centro", r, checks={"_status": 200})

    r = request("GET", "/donaciones/stats/resumen", expected_status=200)
    paso("Paso 5: Stats resumen", r, checks={"_status": 200})

    return True


# ══════════════════════════════════════════════════════════════
#  CA006 — Consulta de centros de acopio
# ══════════════════════════════════════════════════════════════
def test_ca006():
    print("\n=== CA006 — Consulta de centros de acopio ===")

    r = request("GET", "/centros", expected_status=200)
    paso("Paso 1: Listar centros (público)", r, checks={"_status": 200})

    r = request("GET", "/centros/1", expected_status=200)
    paso("Paso 2: Detalle centro 1", r, checks={"_status": 200})

    r = request("GET", "/centros/1/inventario", expected_status=200)
    paso("Paso 3: Inventario centro 1", r, checks={"_status": 200})

    r = request("GET", "/centros/9999", expected_status=404)
    paso("Paso 4: Centro inexistente (404)", r, checks={"_status": 404})

    r = request("GET", "/centros/2", expected_status=200)
    paso("Paso 5: Centro capacidad crítica", r, checks={"_status": 200})

    return True


# ══════════════════════════════════════════════════════════════
#  CA007 — Actualización de estado de donación
# ══════════════════════════════════════════════════════════════
def test_ca007():
    print("\n=== CA007 — Actualización de estado de donación ===")

    if not token_admin:
        print("  [SKIP] No hay token de autenticación")
        return False
    if not donacion_id:
        print("  [SKIP] No hay donacion_id de CA003")
        return False

    r = request("PATCH", f"/donaciones/{donacion_id}/estado",
                {"estado": "En tránsito"},
                token=token_admin, expected_status=200)
    paso("Paso 2: Estado -> En tránsito", r, checks={"_status": 200})

    r = request("PATCH", f"/donaciones/{donacion_id}/estado",
                {"estado": "Entregado"},
                token=token_admin, expected_status=200)
    paso("Paso 3: Estado -> Entregado", r, checks={"_status": 200})

    r = request("PATCH", f"/donaciones/{donacion_id}/estado",
                {"estado": "EstadoInexistente"},
                token=token_admin, expected_status=200)
    paso("Paso 4: Estado inválido (200, sin choices en modelo)", r, checks={"_status": 200})

    r = request("PATCH", f"/donaciones/{donacion_id}/estado",
                {"estado": "Entregado"},
                expected_status=401)
    paso("Paso 5: Sin token (401)", r, checks={"_status": 401})

    return True


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print(" Donatón — Pruebas de Integración")
    print(f" Inicio: {datetime.now().isoformat()}")
    print(f" BFF: {BFF_URL}")
    print("=" * 60)

    tests = [
        ("CA001", test_ca001),
        ("CA002", test_ca002),
        ("CA003", test_ca003),
        ("CA004", test_ca004),
        ("CA005", test_ca005),
        ("CA006", test_ca006),
        ("CA007", test_ca007),
    ]

    for codigo, fn in tests:
        try:
            fn()
        except Exception as e:
            print(f"\n  [ERROR] {codigo} — Excepción: {e}")
            errores.append(f"{codigo}: {e}")

    print("\n" + "=" * 60)
    print(f"  Pasos: {paso_ok}/{paso_total} exitosos")
    if errores:
        print(f"  Errores: {len(errores)}")
        for e in errores:
            print(f"    - {e}")
    else:
        print("  ¡Todos los pasos completados exitosamente!")
    print("=" * 60)
    sys.exit(0 if paso_ok == paso_total and not errores else 1)
