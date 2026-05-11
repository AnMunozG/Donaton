// API Service Layer
// Currently reads/writes localStorage for persistence.
// When the Django REST Framework backend is ready, replace each function body
// with a real fetch() call to the corresponding endpoint.

import {
  tiposRecurso,
  unidadesPorTipo,
  camposPorTipo,
  categoriasDonacion,
  cuentas,
  team,
  valores,
  hitos,
  impactoStats,
  distribucionFondos,
  reportes,
  gobernanza,
  pasosFuncionamiento,
  estadoColor,
  CHART_COLORS,
  urgenciaColorMap,
  estadoNecColorMap,
  loadFromStorage,
  saveToStorage,
} from "./componentes/Datos.jsx";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function request(endpoint, options = {}) {
  // TODO: Replace mock with real fetch when backend is ready
  throw new Error("API not connected — using localStorage mock");
}

// ── Centros ──────────────────────────────────────────────────

export async function getCentros() {
  return Promise.resolve(loadFromStorage("centros") || []);
}

export async function getCentroById(id) {
  const list = loadFromStorage("centros") || [];
  return Promise.resolve(list.find((c) => c.id === id) || null);
}

export async function crearCentro(data) {
  const list = loadFromStorage("centros") || [];
  const nums = list.map((c) => { const m = c.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
  const max = nums.length ? Math.max(...nums) : 0;
  const nuevo = { id: `CA-${String(max + 1).padStart(3, "0")}`, inventario: [], ...data };
  list.push(nuevo);
  saveToStorage("centros", list);
  return Promise.resolve(nuevo);
}

export async function actualizarCentro(id, data) {
  const list = loadFromStorage("centros") || [];
  const idx = list.findIndex((c) => c.id === id);
  if (idx === -1) return Promise.reject(new Error("Centro not found"));
  Object.assign(list[idx], data);
  saveToStorage("centros", list);
  return Promise.resolve(list[idx]);
}

export async function eliminarCentro(id) {
  const list = loadFromStorage("centros") || [];
  saveToStorage("centros", list.filter((c) => c.id !== id));
  return Promise.resolve();
}

// ── Donaciones ───────────────────────────────────────────────

export async function getDonaciones() {
  return Promise.resolve(loadFromStorage("donaciones") || []);
}

export async function crearDonacion(data) {
  const list = loadFromStorage("donaciones") || [];
  const nums = list.map((d) => { const m = d.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
  const max = nums.length ? Math.max(...nums) : 0;
  const nuevo = { id: `DON-${String(max + 1).padStart(3, "0")}`, ...data, estado: data.estado || "En acopio" };
  list.push(nuevo);
  saveToStorage("donaciones", list);
  return Promise.resolve(nuevo);
}

export async function actualizarDonacion(id, data) {
  const list = loadFromStorage("donaciones") || [];
  const idx = list.findIndex((d) => d.id === id);
  if (idx === -1) return Promise.reject(new Error("Donacion not found"));
  Object.assign(list[idx], data);
  saveToStorage("donaciones", list);
  return Promise.resolve(list[idx]);
}

export async function eliminarDonacion(id) {
  const list = loadFromStorage("donaciones") || [];
  saveToStorage("donaciones", list.filter((d) => d.id !== id));
  return Promise.resolve();
}

// ── Necesidades ──────────────────────────────────────────────

export async function getNecesidades() {
  return Promise.resolve(loadFromStorage("necesidades") || []);
}

export async function crearNecesidad(data) {
  const list = loadFromStorage("necesidades") || [];
  const nums = list.map((n) => { const m = n.id?.match(/\d+/); return m ? parseInt(m[0], 10) : 0; }).filter((n) => !isNaN(n));
  const max = nums.length ? Math.max(...nums) : 0;
  const nuevo = { id: `NEC-${String(max + 1).padStart(3, "0")}`, ...data, donado: "0", estado: data.estado || "Pendiente" };
  list.push(nuevo);
  saveToStorage("necesidades", list);
  return Promise.resolve(nuevo);
}

export async function actualizarNecesidad(id, data) {
  const list = loadFromStorage("necesidades") || [];
  const idx = list.findIndex((n) => n.id === id);
  if (idx === -1) return Promise.reject(new Error("Necesidad not found"));
  Object.assign(list[idx], data);
  saveToStorage("necesidades", list);
  return Promise.resolve(list[idx]);
}

export async function eliminarNecesidad(id) {
  const list = loadFromStorage("necesidades") || [];
  saveToStorage("necesidades", list.filter((n) => n.id !== id));
  return Promise.resolve();
}

// ── Envíos ───────────────────────────────────────────────────

export async function getEnvios() {
  return Promise.resolve(loadFromStorage("envios") || []);
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

// ── Login / Cuentas ───────────────────────────────────────────

export async function login(rut, password) {
  const lista = loadFromStorage("cuentas") || cuentas;
  const cuenta = lista.find((c) => c.rut === rut && c.password === password);
  if (!cuenta) throw new Error("Credenciales inválidas");
  return Promise.resolve({ rut, nombre: cuenta.nombre, rol: cuenta.rol, email: cuenta.email || "", token: "mock-token" });
}

export async function crearCuenta(rut, data) {
  const lista = loadFromStorage("cuentas") || [...cuentas];
  if (lista.find((c) => c.rut === rut)) return Promise.reject(new Error("RUT ya registrado"));
  const nueva = { rut, ...data, rol: "user" };
  lista.push(nueva);
  saveToStorage("cuentas", lista);
  return Promise.resolve(nueva);
}

export async function actualizarCuenta(rut, data) {
  const lista = loadFromStorage("cuentas") || [...cuentas];
  const idx = lista.findIndex((c) => c.rut === rut);
  if (idx === -1) return Promise.reject(new Error("Cuenta no encontrada"));
  Object.assign(lista[idx], data);
  saveToStorage("cuentas", lista);
  return Promise.resolve(lista[idx]);
}

// ── Constantes exportadas directamente ────────────────────────

export { estadoColor, CHART_COLORS, urgenciaColorMap, estadoNecColorMap };
export default request;
