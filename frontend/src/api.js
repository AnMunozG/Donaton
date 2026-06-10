import { centrosService } from "./servicios/centros.js";
import { donacionesService } from "./servicios/donaciones.js";
import { necesidadesService } from "./servicios/necesidades.js";
import api from "./servicios/api.js";

// ── Colores y constantes ─────────────────────────────────

export const estadoColor = {
  "Entregado": "#3AB795",
  "En tránsito": "#0dcaf0",
  "En acopio": "#FFC107",
  "Pendiente": "#DD4444",
  "Asignado": "#0d6efd",
  "Cubierto": "#3AB795",
};

export const CHART_COLORS = ["#DD4444", "#F48080", "#3AB795", "#194B4F"];

export const urgenciaColorMap = { Alta: "danger", Media: "warning", Baja: "secondary" };
export const estadoNecColorMap = { Pendiente: "danger", Asignado: "warning", Cubierto: "success" };

// ── Catálogos / Estáticos (desde BFF) ────────────────────

async function fetchStatic(url) {
  const res = await api.get(url);
  return res;
}

export async function getTiposRecurso() {
  const data = await fetchStatic("/static/tipos-recurso");
  return data.map((t) => t.nombre);
}

export async function getUnidadesPorTipo() {
  return fetchStatic("/static/unidades-por-tipo");
}

export async function getCamposPorTipo() {
  return fetchStatic("/static/campos-por-tipo");
}

export async function getCategoriasDonacion() {
  return fetchStatic("/static/categorias-donacion");
}

export async function getPasosFuncionamiento() {
  return fetchStatic("/static/pasos-funcionamiento");
}

export async function getImpactoStats() {
  return fetchStatic("/static/impacto-stats");
}

export async function getDistribucionFondos() {
  return fetchStatic("/static/distribucion-fondos");
}

export async function getReportes() {
  return fetchStatic("/static/reportes");
}

export async function getGobernanza() {
  return fetchStatic("/static/gobernanza");
}

export async function getTeam() {
  return fetchStatic("/static/equipo");
}

export async function getValores() {
  return fetchStatic("/static/valores");
}

export async function getHitos() {
  return fetchStatic("/static/hitos");
}

// ── Centros (solo API — Logistica) ───────────────────────────

export async function getCentros() {
  const data = await centrosService.getAll();
  return Array.isArray(data) ? data : [];
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
  return centrosService.delete(id);
}

// ── Donaciones ───────────────────────────────────────────────

export async function getDonaciones() {
  const data = await donacionesService.getAll();
  return Array.isArray(data) ? data : [];
}

export async function crearDonacion(data) {
  return donacionesService.create(data);
}

export async function actualizarEstadoDonacion(id, estado) {
  return donacionesService.update(id, { estado });
}

export async function actualizarDonacion(id, data) {
  return actualizarEstadoDonacion(id, data.estado);
}

export async function eliminarDonacion(id) {
  return donacionesService.delete(id);
}

// ── Necesidades ──────────────────────────────────────────────

export async function getNecesidades() {
  const data = await necesidadesService.getAll();
  return Array.isArray(data) ? data : [];
}

export async function crearNecesidad(data) {
  return necesidadesService.create(data);
}

export async function actualizarNecesidad(id, data) {
  return necesidadesService.update(id, data);
}

export async function eliminarNecesidad(id) {
  return necesidadesService.delete(id);
}

// ── Necesidades ciudadanas ───────────────────────────────────

export async function getNecesidadesUsuario() {
  try {
    const data = await api.get("/necesidades/ciudadanas");
    return Array.isArray(data) ? data : [];
  } catch {
    return [];
  }
}

export async function agregarNecesidadUsuario(data) {
  return api.post("/necesidades/ciudadanas", data);
}

export async function eliminarNecesidadUsuario(id) {
  await api.delete(`/necesidades/ciudadanas/${id}`);
}

export async function actualizarNecesidadUsuario(id, data) {
  return api.patch(`/necesidades/ciudadanas/${id}`, data);
}

// ── Auth ─────────────────────────────────────────────────────

export async function login(rut, password) {
  return api.post("/auth/login", { rut, password });
}

export async function crearCuenta(rut, data) {
  return api.post("/auth/register", { rut, ...data });
}

export async function actualizarCuenta(rut, data) {
  return api.put("/auth/profile", data);
}
