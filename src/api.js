import { centrosService } from "./servicios/centros.js";
import { donacionesService } from "./servicios/donaciones.js";
import { necesidadesService } from "./servicios/necesidades.js";
import api from "./servicios/api.js";

import {
  tiposRecurso,
  unidadesPorTipo,
  camposPorTipo,
  categoriasDonacion,
  pasosFuncionamiento,
  impactoStats,
  distribucionFondos,
  reportes,
  gobernanza,
  team,
  valores,
  hitos,
  cuentas,
  estadoColor,
  CHART_COLORS,
  urgenciaColorMap,
  estadoNecColorMap,
  loadFromStorage,
  saveToStorage,
  getNecesidadesUsuario as getUserNeeds,
  agregarNecesidadUsuario as addUserNeed,
  eliminarNecesidadUsuario as removeUserNeed,
  actualizarNecesidadUsuario as updateUserNeed,
} from "./componentes/Datos.jsx";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8080/api";

async function request(endpoint, options = {}) {
  const token = localStorage.getItem("donaton_token");
  const headers = { "Content-Type": "application/json", ...options.headers };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${BASE_URL}${endpoint}`, { ...options, headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Error de red");
  return data;
}

function isNetworkError(err) {
  return !err.response || err.code === "ERR_NETWORK" || err.code === "ECONNABORTED";
}

function extraerArray(resp) {
  if (Array.isArray(resp)) return resp;
  if (resp && typeof resp === "object") {
    for (const key of ["centros", "data", "results", "items", "records"]) {
      if (Array.isArray(resp[key])) return resp[key];
    }
  }
  return [];
}

// ── Centros ──────────────────────────────────────────────────

export async function getCentros() {
  try {
    const data = extraerArray(await centrosService.getAll());
    const mock = loadFromStorage("centros") || [];
    return data.map((api) => {
      const m = mock.find((c) => c.nombre === api.nombre);
      if (!m) return api;
      const merged = { ...m };
      for (const k of Object.keys(api)) {
        if (api[k] !== null && api[k] !== undefined && api[k] !== "") merged[k] = api[k];
      }
      merged.id = m.id;
      if (api.coordenadas && (api.coordenadas.lat || api.coordenadas.lng)) merged.coordenadas = api.coordenadas;
      return merged;
    });
  } catch { return loadFromStorage("centros") || []; }
}

export async function getCentroById(id) {
  try { const r = await centrosService.getById(id); return r; } catch { const list = loadFromStorage("centros") || []; return list.find((c) => c.id === id) || null; }
}

export async function crearCentro(data) {
  try { return await centrosService.create(data); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("centros") || [];
    const nums = list.map((c) => { const m = c.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
    const max = nums.length ? Math.max(...nums) : 0;
    const nuevo = { id: `CA-${String(max + 1).padStart(3, "0")}`, inventario: [], ...data };
    list.push(nuevo); saveToStorage("centros", list); return nuevo;
  }
}

export async function actualizarCentro(id, data) {
  try { return await centrosService.update(id, data); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("centros") || [];
    const idx = list.findIndex((c) => c.id === id);
    if (idx === -1) throw new Error("Centro not found");
    Object.assign(list[idx], data); saveToStorage("centros", list); return list[idx];
  }
}

export async function eliminarCentro(id) {
  try { return await centrosService.delete(id); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("centros") || [];
    saveToStorage("centros", list.filter((c) => c.id !== id));
  }
}

// ── Donaciones ───────────────────────────────────────────────

export async function getDonaciones() {
  try { return extraerArray(await donacionesService.getAll()); } catch { return loadFromStorage("donaciones") || []; }
}

export async function crearDonacion(data) {
  try { return await donacionesService.create(data); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("donaciones") || [];
    const nums = list.map((d) => { const m = d.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
    const max = nums.length ? Math.max(...nums) : 0;
    const nuevo = { id: `DON-${String(max + 1).padStart(3, "0")}`, ...data, estado: data.estado || "En acopio" };
    list.push(nuevo); saveToStorage("donaciones", list); return nuevo;
  }
}

export async function actualizarDonacion(id, data) {
  try { return await donacionesService.update(id, data); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("donaciones") || [];
    const idx = list.findIndex((d) => d.id === id);
    if (idx === -1) throw new Error("Donacion not found");
    Object.assign(list[idx], data); saveToStorage("donaciones", list); return list[idx];
  }
}

export async function eliminarDonacion(id) {
  try { return await donacionesService.delete(id); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("donaciones") || [];
    saveToStorage("donaciones", list.filter((d) => d.id !== id));
  }
}

// ── Necesidades (API + localStorage) ─────────────────────────

export async function getNecesidades() {
  try { return extraerArray(await necesidadesService.getAll()); } catch { return loadFromStorage("necesidades") || []; }
}

export async function crearNecesidad(data) {
  try { return await necesidadesService.create(data); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("necesidades") || [];
    const nums = list.map((n) => { const m = n.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
    const max = nums.length ? Math.max(...nums) : 0;
    const nuevo = { id: `NEC-${String(max + 1).padStart(3, "0")}`, ...data, donado: "0", estado: data.estado || "Pendiente" };
    list.push(nuevo); saveToStorage("necesidades", list); return nuevo;
  }
}

export async function actualizarNecesidad(id, data) {
  try { return await necesidadesService.update(id, data); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("necesidades") || [];
    const idx = list.findIndex((n) => n.id === id);
    if (idx === -1) throw new Error("Necesidad not found");
    Object.assign(list[idx], data); saveToStorage("necesidades", list); return list[idx];
  }
}

export async function eliminarNecesidad(id) {
  try { return await necesidadesService.delete(id); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const list = loadFromStorage("necesidades") || [];
    saveToStorage("necesidades", list.filter((n) => n.id !== id));
  }
}

// ── Envíos (API + localStorage) ──────────────────────────────

export async function getEnvios() {
  try { return extraerArray(await api.get("/envios")); } catch { return loadFromStorage("envios") || []; }
}

// ── Auth ─────────────────────────────────────────────────────

export async function login(rut, password) {
  try { return await api.post("/auth/login", { rut, password }); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const lista = loadFromStorage("cuentas") || cuentas;
    const cuenta = lista.find((c) => c.rut === rut && c.password === password);
    if (!cuenta) throw new Error("Credenciales inválidas");
    return { rut, nombre: cuenta.nombre, rol: cuenta.rol, email: cuenta.email || "", token: "mock-token" };
  }
}

export async function crearCuenta(rut, data) {
  try { return await api.post("/auth/register", { rut, ...data }); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const lista = loadFromStorage("cuentas") || [...cuentas];
    if (lista.find((c) => c.rut === rut)) throw new Error("RUT ya registrado");
    const nueva = { rut, ...data, rol: "user" };
    lista.push(nueva); saveToStorage("cuentas", lista); return nueva;
  }
}

export async function actualizarCuenta(rut, data) {
  try { return await api.put("/auth/profile", data); } catch (e) {
    if (!isNetworkError(e)) throw e;
    const lista = loadFromStorage("cuentas") || [...cuentas];
    const idx = lista.findIndex((c) => c.rut === rut);
    if (idx === -1) throw new Error("Cuenta no encontrada");
    Object.assign(lista[idx], data); saveToStorage("cuentas", lista); return lista[idx];
  }
}

// ── Catálogos / Estáticos ───────────────────────────────────

export async function getTiposRecurso() { return Promise.resolve(tiposRecurso); }
export async function getUnidadesPorTipo() { return Promise.resolve(unidadesPorTipo); }
export async function getCamposPorTipo() { return Promise.resolve(camposPorTipo); }
export async function getCategoriasDonacion() { return Promise.resolve(categoriasDonacion); }
export async function getPasosFuncionamiento() { return Promise.resolve(pasosFuncionamiento); }

// ── Transparencia ────────────────────────────────────────────

export async function getImpactoStats() { return Promise.resolve(impactoStats); }
export async function getDistribucionFondos() { return Promise.resolve(distribucionFondos); }
export async function getReportes() { return Promise.resolve(reportes); }
export async function getGobernanza() { return Promise.resolve(gobernanza); }

// ── Nosotros ─────────────────────────────────────────────────

export async function getTeam() { return Promise.resolve(team); }
export async function getValores() { return Promise.resolve(valores); }
export async function getHitos() { return Promise.resolve(hitos); }

// ── Constantes exportadas directamente ────────────────────────

export { estadoColor, CHART_COLORS, urgenciaColorMap, estadoNecColorMap };
export default request;
