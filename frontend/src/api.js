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

// ── Centros (solo API — Logistica) ───────────────────────────

export async function getCentros() {
  return extraerArray(await centrosService.getAll());
}

export async function getCentroById(id) {
  return centrosService.getById(id);
}

export async function crearCentro(data) {
  return centrosService.create(data);
}

export async function actualizarCentro(id, data) {
  return centrosService.update(id, data);
}

export async function eliminarCentro(id) {
  try { return await centrosService.delete(id); } catch (e) {
    const list = loadFromStorage("centros") || [];
    saveToStorage("centros", list.filter((c) => c.id !== id));
    return { deleted: true };
  }
}

// ── Donaciones ───────────────────────────────────────────────

export async function getDonaciones() {
  try { return extraerArray(await donacionesService.getAll()); } catch { return loadFromStorage("donaciones") || []; }
}

export async function crearDonacion(data) {
  try { return await donacionesService.create(data); } catch {
    const list = loadFromStorage("donaciones") || [];
    const nums = list.map((d) => { const m = d.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
    const max = nums.length ? Math.max(...nums) : 0;
    const nuevo = { id: `DON-${String(max + 1).padStart(3, "0")}`, ...data, estado: data.estado || "En acopio" };
    list.push(nuevo); saveToStorage("donaciones", list); return nuevo;
  }
}

export async function actualizarEstadoDonacion(id, estado) {
  try { return await donacionesService.update(id, { estado }); } catch {
    const list = loadFromStorage("donaciones") || [];
    const idx = list.findIndex((d) => d.id === id);
    if (idx === -1) throw new Error("Donacion not found");
    list[idx].estado = estado; saveToStorage("donaciones", list); return list[idx];
  }
}

export async function actualizarDonacion(id, data) {
  const estado = data.estado;
  return actualizarEstadoDonacion(id, estado);
}

export async function eliminarDonacion(id) {
  const list = loadFromStorage("donaciones") || [];
  saveToStorage("donaciones", list.filter((d) => d.id !== id));
}

// ── Necesidades (API + localStorage) ─────────────────────────

export async function getNecesidades() {
  try { return extraerArray(await necesidadesService.getAll()); } catch { return loadFromStorage("necesidades") || []; }
}

export async function crearNecesidad(data) {
  try { return await necesidadesService.create(data); } catch {
    const list = loadFromStorage("necesidades") || [];
    const nums = list.map((n) => { const m = n.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
    const max = nums.length ? Math.max(...nums) : 0;
    const nuevo = { id: `NEC-${String(max + 1).padStart(3, "0")}`, ...data, donado: "0", estado: data.estado || "Pendiente" };
    list.push(nuevo); saveToStorage("necesidades", list); return nuevo;
  }
}

export async function actualizarNecesidad(id, data) {
  try { return await necesidadesService.update(id, data); } catch {
    const list = loadFromStorage("necesidades") || [];
    const idx = list.findIndex((n) => n.id === id);
    if (idx === -1) throw new Error("Necesidad not found");
    Object.assign(list[idx], data); saveToStorage("necesidades", list); return list[idx];
  }
}

export async function eliminarNecesidad(id) {
  const list = loadFromStorage("necesidades") || [];
  saveToStorage("necesidades", list.filter((n) => n.id !== id));
}

// ── Auth ─────────────────────────────────────────────────────

export async function login(rut, password) {
  const res = await api.post("/auth/login", { rut, password });
  return res;
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
