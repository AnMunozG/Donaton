import { useState, useEffect, useMemo } from "react";
import { validarRequerido, validarEnteroPositivo, validarRut, validarForm, formatearRut, limpiarRut, capacidadColor } from "../componentes/Validaciones.js";
import RichTextEditor from "../componentes/RichTextEditor";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from "recharts";
import {
  getDonaciones, getNecesidades, getCentros,
  crearDonacion, actualizarDonacion, eliminarDonacion,
  crearNecesidad, actualizarNecesidad, eliminarNecesidad,
  crearCentro, actualizarCentro, eliminarCentro,
  getNecesidadesUsuario, eliminarNecesidadUsuario, actualizarNecesidadUsuario,
  activarNecesidad,
  crearAgradecimiento,
  getUsuarios, actualizarUsuario,
  getVoluntarios, actualizarVoluntario, eliminarVoluntario,
  cambiarEstadoVoluntario,
  registrarHorasVoluntario, getHorasVoluntario,
  actualizarCentroVoluntario,
  enviarNotificacion, getHabilidadesVoluntario,
  estadoColor, CHART_COLORS,
} from "../api.js";
import { centrosService } from "../servicios/centros.js";
import SelectRegion from "../componentes/SelectRegion";
import AddressPicker from "../componentes/AddressPicker";
import { useAuth } from "../componentes/AuthContext";

const tabs = [
  { id: "dashboard", label: "Dashboard", icon: "bi-speedometer2" },
  { id: "donaciones", label: "Donaciones", icon: "bi-gift-fill" },
  { id: "necesidades", label: "Necesidades", icon: "bi-exclamation-triangle-fill" },
  { id: "centros", label: "Centros", icon: "bi-building-fill" },
  { id: "voluntarios", label: "Voluntarios", icon: "bi-person-arms-up" },
  { id: "usuarios", label: "Usuarios", icon: "bi-people-fill" },
];

const estadosDonacion = ["Donación Registrada", "En Recolección", "En transporte", "Recibida"];
const urgencias = ["Alta", "Media", "Baja"];

function emptyForm(entity) {
  if (entity === "donacion") return { tipo: "", cantidad: "", unidad: "", origen: "", centroId: "", estado: "Donación Registrada", tipoPersonalizado: "" };
  if (entity === "necesidad") return { recurso: "", cantidad: "", unidad: "", urgencia: "Media", estado: "Pendiente", centroId: "", reportadoPor: "", descripcion: "" };
  return { nombre: "", region: "", direccion: "", telefono: "", encargado: "", latitud: "", longitud: "", capacidadTotal: "", capacidadUsada: "", estado: "Activo" };
}

export default function BackOffice() {
  const { user } = useAuth();
  const esEncargado = user?.rol === "encargado";
  const esAdmin = user?.rol === "admin";

  const [donaciones, setDonaciones] = useState([]);
  const [necesidades, setNecesidades] = useState([]);
  const [centros, setCentros] = useState([]);
  const [activeTab, setActiveTab] = useState(esEncargado ? "dashboard" : "dashboard");
  const [filtroEstado, setFiltroEstado] = useState("Todas");
  const [centroSeleccionado, setCentroSeleccionado] = useState(null);

  const [showModal, setShowModal] = useState(false);
  const [modalEntity, setModalEntity] = useState(null);
  const [editItem, setEditItem] = useState(null);
  const [form, setForm] = useState({});
  const [formErrors, setFormErrors] = useState({});
  const [userNeeds, setUserNeeds] = useState([]);
  const [userNecKey, setUserNecKey] = useState(0);
  const [showAgradecerModal, setShowAgradecerModal] = useState(false);
  const [agradecerDonacion, setAgradecerDonacion] = useState(null);
  const [agradecerMensaje, setAgradecerMensaje] = useState("");
  const [agradecerEnviando, setAgradecerEnviando] = useState(false);

  const [usuarios, setUsuarios] = useState([]);
  const [usuariosKey, setUsuariosKey] = useState(0);

  const [voluntarios, setVoluntarios] = useState([]);
  const [voluntariosKey, setVoluntariosKey] = useState(0);
  const [showHorasModal, setShowHorasModal] = useState(false);
  const [horasVoluntario, setHorasVoluntario] = useState(null);
  const [horasForm, setHorasForm] = useState({ horas: "", descripcion: "" });
  const [horasData, setHorasData] = useState(null);
  const [filtroVoluntarioCentro, setFiltroVoluntarioCentro] = useState("");
  const [horasCentroSeleccionado, setHorasCentroSeleccionado] = useState("");
  const [habilidadesVol, setHabilidadesVol] = useState([]);
  const [notifModal, setNotifModal] = useState({ show: false, voluntario: null });
  const [notifForm, setNotifForm] = useState({ titulo: "", mensaje: "" });
  const [notifEnviando, setNotifEnviando] = useState(false);

  const voluntariosPendientes = voluntarios.reduce((count, v) => {
    return count + (v.centros || []).filter((c) => c.estado === "pendiente").length;
  }, 0);

  const tabsDisponibles = esEncargado
    ? tabs.filter((t) => t.id !== "usuarios")
    : tabs;

  useEffect(() => {
    getDonaciones().then(setDonaciones);
    getNecesidades().then(setNecesidades);
    getCentros().then(setCentros);
    getHabilidadesVoluntario().then(setHabilidadesVol);
  }, []);

  useEffect(() => {
    if (esAdmin) getUsuarios().then(setUsuarios);
  }, [esAdmin, usuariosKey]);

  useEffect(() => {
    getVoluntarios().then(setVoluntarios);
  }, [voluntariosKey]);

  useEffect(() => {
    getNecesidadesUsuario().then(setUserNeeds);
  }, [userNecKey]);

  const donacionesFiltradas = filtroEstado === "Todas"
    ? donaciones
    : donaciones.filter((d) => d.estado === filtroEstado);

  const donacionesPorEstado = useMemo(() => {
    const counts = {};
    donaciones.forEach((d) => { counts[d.estado] = (counts[d.estado] || 0) + 1; });
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [donaciones]);

  const donacionesPorTipo = useMemo(() => {
    const counts = {};
    donaciones.forEach((d) => { counts[d.tipo] = (counts[d.tipo] || 0) + 1; });
    return Object.entries(counts).map(([name, cantidad]) => ({ name, cantidad }));
  }, [donaciones]);

  const necesidadesPendientes = necesidades.filter((n) => n.estado !== "Cubierta").length;
  const totalCapacidad = centros.reduce((a, c) => a + c.capacidadTotal, 0);
  const capacidadUsada = centros.reduce((a, c) => a + c.capacidadUsada, 0);

  const necesidadesPorCentro = useMemo(() => {
    const counts = {};
    necesidades.forEach((n) => {
      if (n.centroId) {
        const centro = centros.find((c) => c.id === n.centroId);
        const nombre = centro ? centro.nombre : n.centroId;
        counts[nombre] = (counts[nombre] || 0) + 1;
      }
    });
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [necesidades, centros]);

  const estados = ["Todas", ...new Set(donaciones.map((d) => d.estado))];

  const openCreate = (entity) => {
    setModalEntity(entity);
    setEditItem(null);
    setForm(emptyForm(entity));
    setFormErrors({});
    setShowModal(true);
  };

  const openEdit = (entity, item) => {
    setModalEntity(entity);
    setEditItem(item);
    setForm({ ...item });
    setFormErrors({});
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setModalEntity(null);
    setEditItem(null);
    setForm({});
    setFormErrors({});
  };

  const handleFormChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (formErrors[e.target.name]) setFormErrors({ ...formErrors, [e.target.name]: "" });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    const entity = modalEntity;
    const reglas = entity === "donacion" ? [
      { campo: "tipo", nombre: "Tipo", validaciones: [validarRequerido] },
      { campo: "cantidad", nombre: "Cantidad", validaciones: [validarRequerido, validarEnteroPositivo] },
      { campo: "unidad", nombre: "Unidad", validaciones: [validarRequerido] },
      { campo: "origen", nombre: "Origen (RUT)", validaciones: [validarRequerido, validarRut] },
      { campo: "centroId", nombre: "Centro", validaciones: [validarRequerido] },
    ] : entity === "necesidad" ? [
      { campo: "recurso", nombre: "Recurso", validaciones: [validarRequerido] },
      { campo: "cantidad", nombre: "Cantidad", validaciones: [validarRequerido, validarEnteroPositivo] },
      { campo: "unidad", nombre: "Unidad", validaciones: [validarRequerido] },
      { campo: "centroId", nombre: "Centro destino", validaciones: [validarRequerido] },
      { campo: "reportadoPor", nombre: "Reportado por", validaciones: [validarRequerido] },
    ] : entity === "centro" ? [
      { campo: "nombre", nombre: "Nombre", validaciones: [validarRequerido] },
      { campo: "region", nombre: "Región", validaciones: [validarRequerido] },
      { campo: "capacidadTotal", nombre: "Capacidad total", validaciones: [validarRequerido, validarEnteroPositivo] },
    ] : [];
    const errores = validarForm(form, reglas);
    if (entity === "centro" && form.capacidadUsada !== "" && form.capacidadTotal !== "") {
      const usada = parseInt(form.capacidadUsada, 10) || 0;
      const total = parseInt(form.capacidadTotal, 10) || 0;
      if (usada > total) errores.capacidadUsada = "No puede superar la capacidad total";
    }
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;
    if (entity === "donacion") {
      if (editItem) {
        await actualizarDonacion(editItem.id, { estado: form.estado });
      } else {
        const tipoFinal = form.tipo === "Otros" && form.tipoPersonalizado
          ? `Otros - ${form.tipoPersonalizado}`
          : form.tipo;
        await crearDonacion({
          tipo: tipoFinal,
          cantidad: form.cantidad,
          unidad: form.unidad,
          origen: form.origen,
          centroId: form.centroId,
          fecha: new Date().toISOString().split("T")[0],
        });
      }
      getDonaciones().then(setDonaciones);
    } else if (entity === "necesidad") {
      if (editItem) {
        await actualizarNecesidad(editItem.id, {
          cantidad: form.cantidad,
          urgencia: form.urgencia,
          estado: form.estado,
          descripcion: form.descripcion,
          reportadoPor: form.reportadoPor,
        });
      } else {
        await crearNecesidad({
          centroId: form.centroId,
          recurso: form.recurso,
          cantidad: form.cantidad,
          unidad: form.unidad,
          descripcion: form.descripcion || "",
          urgencia: form.urgencia || "Media",
          reportadoPor: form.reportadoPor || "",
        });
      }
      getNecesidades().then(setNecesidades);
    } else if (entity === "centro") {
      const coordenadas = (form.latitud && form.longitud)
        ? { lat: parseFloat(form.latitud), lng: parseFloat(form.longitud) }
        : undefined;
      const payload = {
        nombre: form.nombre,
        region: form.region,
        direccion: form.direccion || "",
        telefono: form.telefono || "",
        encargado: form.encargado || "",
        capacidadTotal: parseInt(form.capacidadTotal, 10) || 0,
        ...(coordenadas ? { coordenadas } : {}),
      };
      if (form.capacidadUsada !== "") {
        payload.capacidadUsada = parseInt(form.capacidadUsada, 10);
      }
      if (editItem) {
        payload.estado = form.estado || "Activo";
        await actualizarCentro(editItem.id, payload);
      } else {
        await crearCentro(payload);
      }
      getCentros().then(setCentros);
    }
    closeModal();
  };

  const handleDelete = (entity, id) => {
    if (!window.confirm(`¿Eliminar ${id}? Esta acción no se puede deshacer.`)) return;
    if (entity === "donacion") {
      eliminarDonacion(id).then(() => getDonaciones().then(setDonaciones));
    } else if (entity === "necesidad") {
      eliminarNecesidad(id).then(() => getNecesidades().then(setNecesidades));
    } else if (entity === "centro") {
      eliminarCentro(id).then(() => getCentros().then(setCentros));
    }
  };

  const handleUrgenciaChange = async (id, value) => {
    await actualizarNecesidad(id, { urgencia: value });
    getNecesidades().then(setNecesidades);
  };

  const handleActivarNecesidad = async (userNeed) => {
    if (!userNeed.urgencia) {
      alert("Debe asignar un nivel de urgencia antes de activar la necesidad.");
      return;
    }
    await activarNecesidad(userNeed.id, userNeed.urgencia);
    getNecesidades().then(setNecesidades);
    setUserNecKey((k) => k + 1);
  };

  const BadgeEstado = ({ estado }) => (
    <span className="bo-badge badge-dynamic"
      style={{
        '--badge-bg': `${estadoColor[estado] || "#6c757d"}18`,
        '--badge-color': estadoColor[estado] || "#6c757d",
        '--badge-border': `${estadoColor[estado] || "#6c757d"}35`,
      }}>
      {estado}
    </span>
  );

  const rechartsTooltip = { background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 8, color: "var(--text)" };

  return (
    <div className="backoffice-page">
      <div className="bo-layout">

        {/* SIDEBAR */}
        <aside className="bo-sidebar">
          <div className="bo-sidebar-header">
            <i className="bi bi-shield-fill-check fs-4 c-primary"></i>
            <span className="fw-bold c-heading">Admin Panel</span>
          </div>

          <nav className="bo-nav">
            {tabsDisponibles.map((tab) => {
              const pendientes = tab.id === "voluntarios"
                ? voluntarios.filter((v) => v.estado === "pendiente").length
                : 0;
              return (
                <button key={tab.id}
                  className={`bo-nav-btn${activeTab === tab.id ? " active" : ""}`}
                  onClick={() => setActiveTab(tab.id)}>
                  <i className={`bi ${tab.icon}`}></i>
                  <span>{tab.label}</span>
                  {pendientes > 0 && (
                    <span className="badge bg-danger ms-1 badge-xs">{pendientes}</span>
                  )}
                </button>
              );
            })}
          </nav>

          <div className="bo-sidebar-footer">
            <small className="c-muted">Donatón v1.0</small>
          </div>
        </aside>

        {/* MAIN */}
        <main className="bo-main">

          {/* DASHBOARD */}
          {activeTab === "dashboard" && (
            <>

              <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="m-0 c-heading">
                  <i className="bi bi-speedometer2 me-2 c-primary"></i>Dashboard
                </h2>
                <span className="bo-date-badge">
                  <i className="bi bi-calendar3 me-1"></i>
                  {new Date().toLocaleDateString("es-CL", { year: "numeric", month: "long", day: "numeric" })}
                </span>
              </div>

              <div className="row g-3 mb-4">
                {[
                  { icon: "bi-gift-fill", label: "Donaciones totales", value: donaciones.length, color: "#DD4444", bg: "rgba(221,68,68,0.1)" },
                  { icon: "bi-exclamation-triangle-fill", label: "Necesidades activas", value: necesidadesPendientes, color: "#FFC107", bg: "rgba(255,193,7,0.1)" },
                  { icon: "bi-building-fill", label: "Centros de acopio", value: centros.length, color: "#3AB795", bg: "rgba(58,183,149,0.1)" },
                  { icon: "bi-box-seam-fill", label: "Capacidad utilizada", value: `${Math.round((capacidadUsada / totalCapacidad) * 100)}%`, color: "#0dcaf0", bg: "rgba(13,202,240,0.1)" },
                ].map((card, i) => (
                  <div key={i} className="col-sm-6 col-xl-3">
                    <div className="bo-card card-accent-left" style={{ '--accent-color': card.color }}>
                      <div className="d-flex justify-content-between align-items-start">
                        <div>
                          <div className="bo-card-label">{card.label}</div>
                          <div className="bo-card-value">{card.value}</div>
                        </div>
                        <div className="bo-card-icon card-icon-dynamic" style={{ '--icon-bg': card.bg, '--icon-color': card.color }}>
                          <i className={`bi ${card.icon}`}></i>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="row g-3 mb-4">
                <div className="col-lg-8">
                  <div className="bo-chart-card">
                    <h5 className="mb-3 c-heading">
                      <i className="bi bi-bar-chart-fill me-2 c-primary"></i>Donaciones por tipo
                    </h5>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={donacionesPorTipo}>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                        <XAxis dataKey="name" tick={{ fill: "var(--text-muted)", fontSize: 12 }} angle={-20} textAnchor="end" height={60} />
                        <YAxis tick={{ fill: "var(--text-muted)", fontSize: 12 }} />
                        <Tooltip contentStyle={rechartsTooltip} />
                        <Bar dataKey="cantidad" fill="#DD4444" radius={[6, 6, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="col-lg-4">
                  <div className="bo-chart-card h-100">
                    <h5 className="mb-3 c-heading">
                      <i className="bi bi-pie-chart-fill me-2 c-primary"></i>Estado donaciones
                    </h5>
                    <ResponsiveContainer width="100%" height={280}>
                      <PieChart>
                        <Pie data={donacionesPorEstado} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} innerRadius={40}>
                          {donacionesPorEstado.map((_, idx) => (
                            <Cell key={idx} fill={CHART_COLORS[idx % CHART_COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip contentStyle={rechartsTooltip} />
                        <Legend wrapperStyle={{ fontSize: 12, color: "var(--text-muted)" }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              <div className="bo-chart-card">
                <h5 className="mb-3 c-heading">
                  <i className="bi bi-geo-alt-fill me-2 c-primary"></i>Necesidades por centro
                </h5>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={necesidadesPorCentro} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                    <XAxis type="number" tick={{ fill: "var(--text-muted)", fontSize: 12 }} />
                    <YAxis type="category" dataKey="name" tick={{ fill: "var(--text-muted)", fontSize: 12 }} width={140} />
                    <Tooltip contentStyle={rechartsTooltip} />
                    <Bar dataKey="value" fill="#F48080" radius={[0, 6, 6, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

            </>
          )}

          {/* DONACIONES */}
          {activeTab === "donaciones" && (
            <>

              <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
                <h2 className="m-0 c-heading">
                  <i className="bi bi-gift-fill me-2 c-primary"></i>Donaciones
                </h2>
                <div className="d-flex gap-2 align-items-center">
                  <label className="form-label m-0 small c-muted">Filtrar:</label>
                  <select className="form-select form-select-sm w-auto" value={filtroEstado} onChange={(e) => setFiltroEstado(e.target.value)}>
                    {estados.map((est) => <option key={est} value={est}>{est}</option>)}
                  </select>
                  <button className="btn btn-sm btn-success" onClick={() => openCreate("donacion")}>
                    <i className="bi bi-plus-lg me-1"></i>Crear
                  </button>
                </div>
              </div>

              <div className="bo-table-wrapper">
                <table className="bo-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Tipo</th>
                      <th>Cantidad</th>
                      <th>Origen</th>
                      <th>Centro</th>
                      <th>Fecha</th>
                      <th>Estado</th>
                      <th className="bo-actions-th">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {donacionesFiltradas.map((d) => (
                      <tr key={d.id}>
                        <td><span className="bo-id">{d.id}</span></td>
                        <td className="fw-medium">{d.tipo}</td>
                        <td>{d.cantidad} {d.unidad}</td>
                        <td>{d.origen}</td>
                        <td>{d.centro}</td>
                        <td>{d.fecha}</td>
                        <td><BadgeEstado estado={d.estado} /></td>
                        <td>
                          <div className="d-flex gap-1">
                            <button className="btn btn-sm btn-outline-primary py-0 px-1" title="Editar" onClick={() => openEdit("donacion", d)}>
                              <i className="bi bi-pencil"></i>
                            </button>
                            {!esEncargado && (
                              <button className="btn btn-sm btn-outline-danger py-0 px-1" title="Eliminar" onClick={() => handleDelete("donacion", d.id)}>
                                <i className="bi bi-trash"></i>
                              </button>
                            )}
                            <button className="btn btn-sm btn-outline-success py-0 px-1" title="Agradecer" onClick={() => { setAgradecerDonacion(d); setAgradecerMensaje(""); setShowAgradecerModal(true); }}>
                              <i className="bi bi-heart-fill"></i>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

            </>
          )}

          {/* NECESIDADES */}
          {activeTab === "necesidades" && (
            <div key={userNecKey}>

              <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="m-0 c-heading">
                  <i className="bi bi-exclamation-triangle-fill me-2 c-primary"></i>Necesidades
                </h2>
                <button className="btn btn-sm btn-success" onClick={() => openCreate("necesidad")}>
                  <i className="bi bi-plus-lg me-1"></i>Crear
                </button>
              </div>

              {/* Pendientes de revisión */}
              {userNeeds.length > 0 && (
                <div className="mb-4">
                  <h5 className="c-heading mb-2">
                    <i className="bi bi-clock-history me-2 c-warning"></i>Pendientes de revisión
                    <span className="badge bg-warning text-dark ms-2">{userNeeds.length}</span>
                  </h5>
                  <div className="bo-table-wrapper">
                    <table className="bo-table">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Recurso</th>
                          <th>Cantidad</th>
                          <th>Centro destino</th>
                          <th>Urgencia</th>
                          <th>Estado</th>
                          <th>Reportado por</th>
                    <th className="bo-actions-th">Acciones</th>
                        </tr>
                      </thead>
                      <tbody>
                        {userNeeds.map((n) => {
                          const centroNec = centros.find((c) => c.id === n.centroId);
                          return (
                            <tr key={n.id}>
                              <td><span className="bo-id">{n.id}</span></td>
                              <td className="fw-medium">{n.recurso}</td>
                              <td>{n.cantidad} {n.unidad}</td>
                              <td>{centroNec ? centroNec.nombre : n.centro || "—"}</td>
                              <td>
                                <select className="form-select form-select-sm bo-select-sm"
                                  value={n.urgencia || ""}
                                  onChange={(e) => {
                                    actualizarNecesidadUsuario(n.id, { urgencia: e.target.value });
                                    setUserNecKey((k) => k + 1);
                                  }}>
                                  <option value="">Asignar</option>
                                  <option value="Alta">Alta</option>
                                  <option value="Media">Media</option>
                                  <option value="Baja">Baja</option>
                                </select>
                              </td>
                              <td><BadgeEstado estado={n.estado} /></td>
                              <td>{n.reportadoPor}</td>
                              <td>
                                <div className="d-flex gap-1">
                                  <button className="btn btn-sm btn-outline-success py-0 px-1" title="Activar"
                                    onClick={() => handleActivarNecesidad(n)}>
                                    <i className="bi bi-check-lg"></i>
                                  </button>
                                  <button className="btn btn-sm btn-outline-danger py-0 px-1" title="Eliminar"
                                    onClick={() => { eliminarNecesidadUsuario(n.id); setUserNecKey((k) => k + 1); }}>
                                    <i className="bi bi-trash"></i>
                                  </button>
                                </div>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Necesidades activas */}
              <div>
                <h5 className="c-heading mb-2">
                  <i className="bi bi-list-check me-2 c-primary"></i>Necesidades activas
                </h5>
                <div className="bo-table-wrapper">
                  <table className="bo-table">
                    <thead>
                      <tr>
                        <th>ID</th>
                        <th>Recurso</th>
                        <th>Cantidad</th>
                        <th>Centro destino</th>
                        <th>Urgencia</th>
                        <th>Estado</th>
                        <th>Reportado por</th>
                        <th className="bo-actions-th">Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {necesidades.filter((n) => n.estado !== "Pendiente").map((n) => {
                        const centroNec = centros.find((c) => c.id === n.centroId);
                        return (
                          <tr key={n.id}>
                            <td><span className="bo-id">{n.id}</span></td>
                            <td className="fw-medium">{n.recurso}</td>
                            <td>{n.cantidad} {n.unidad}</td>
                            <td>{centroNec ? centroNec.nombre : n.centro || "—"}</td>
                            <td>
                              <select className="form-select form-select-sm bo-select-sm"
                                value={n.urgencia}
                                onChange={(e) => handleUrgenciaChange(n.id, e.target.value)}>
                                <option value="Alta">Alta</option>
                                <option value="Media">Media</option>
                                <option value="Baja">Baja</option>
                              </select>
                            </td>
                            <td><BadgeEstado estado={n.estado} /></td>
                            <td>{n.reportadoPor}</td>
                            <td>
                              <div className="d-flex gap-1">
                                <button className="btn btn-sm btn-outline-primary py-0 px-1" title="Editar" onClick={() => openEdit("necesidad", n)}>
                                  <i className="bi bi-pencil"></i>
                                </button>
                                {!esEncargado && (
                                  <button className="btn btn-sm btn-outline-danger py-0 px-1" title="Eliminar" onClick={() => handleDelete("necesidad", n.id)}>
                                    <i className="bi bi-trash"></i>
                                  </button>
                                )}
                              </div>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          )}

          {/* CENTROS */}
          {activeTab === "centros" && (
            <>

              <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="m-0 c-heading">
                  <i className="bi bi-building-fill me-2 c-primary"></i>Centros de acopio
                </h2>
                {!esEncargado && (
                  <button className="btn btn-sm btn-success" onClick={() => openCreate("centro")}>
                    <i className="bi bi-plus-lg me-1"></i>Crear
                  </button>
                )}
              </div>

              <div className="bo-table-wrapper">
                <table className="bo-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nombre</th>
                      <th>Región</th>
                      <th>Encargado</th>
                      <th>Capacidad</th>
                      <th>Uso</th>
                      <th>Estado</th>
                      <th className="bo-actions-th">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {centros.map((c) => {
                      const pct = Math.round((c.capacidadUsada / c.capacidadTotal) * 100);
                      const isSelected = centroSeleccionado?.id === c.id;
                      const handleSelect = async () => {
                        if (isSelected) { setCentroSeleccionado(null); return; }
                        try {
                          const inv = await centrosService.getInventario(c.id);
                          setCentroSeleccionado({ ...c, inventario: inv });
                        } catch { setCentroSeleccionado({ ...c, inventario: [] }); }
                      };
                      return (
                        <tr key={c.id}
                          className={isSelected ? "bo-row-selected" : "bo-row"}
                          onClick={handleSelect}>
                          <td><span className="bo-id">{c.id}</span></td>
                          <td className="fw-medium">{c.nombre}</td>
                          <td>{c.region}</td>
                          <td>{c.encargado || "—"}</td>
                          <td>{c.capacidadTotal} unid.</td>
                          <td>
                            <div className="d-flex align-items-center gap-2">
                              <div className="bo-progress">
                                <div className="bo-progress-bar progress-dynamic-bar" style={{ '--bar-w': `${pct}%`, '--bar-color': capacidadColor(pct) }}></div>
                              </div>
                              <small className="c-muted">{pct}%</small>
                            </div>
                          </td>
                          <td><span className="bo-badge badge-dynamic" style={{ '--badge-bg': c.estado === "Activo" ? "rgba(58,183,149,0.12)" : "rgba(221,68,68,0.12)", '--badge-color': c.estado === "Activo" ? "#3AB795" : "#DD4444" }}>{c.estado}</span></td>
                          <td onClick={(e) => e.stopPropagation()}>
                            <div className="d-flex gap-1">
                              <button className="btn btn-sm btn-outline-primary py-0 px-1" title="Editar" onClick={() => openEdit("centro", c)}>
                                <i className="bi bi-pencil"></i>
                              </button>
                              {!esEncargado && (
                                <button className="btn btn-sm btn-outline-danger py-0 px-1" title="Eliminar" onClick={() => handleDelete("centro", c.id)}>
                                  <i className="bi bi-trash"></i>
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {centroSeleccionado && (
                <div className="bo-chart-card mt-4">
                  <h5 className="mb-3 c-heading">
                    <i className="bi bi-box-seam-fill me-2 c-primary"></i>
                    Inventario — {centroSeleccionado.nombre}
                  </h5>
                  <div className="row g-3">
                    {centroSeleccionado.inventario.map((item, i) => (
                      <div key={i} className="col-sm-6 col-md-4 col-lg-3">
                        <div className="bo-card">
                          <div className="bo-card-label">{item.tipo}</div>
                          <div className="bo-card-value">{item.cantidad}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

            </>
          )}

          {/* VOLUNTARIOS */}
          {activeTab === "voluntarios" && (
            <>
              <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="m-0 c-heading">
                  <i className="bi bi-person-arms-up me-2 c-primary"></i>Voluntarios
                </h2>
                <div className="d-flex gap-2 align-items-center">
                  <select className="form-select form-select-sm bo-select-auto"
                    value={filtroVoluntarioCentro}
                    onChange={(e) => setFiltroVoluntarioCentro(e.target.value)}>
                    <option value="">Todos los centros</option>
                    {centros.map((c) => (
                      <option key={c.id} value={c.id}>{c.nombre}</option>
                    ))}
                  </select>
                </div>
              </div>

              {voluntariosPendientes > 0 && (
                <div className="alert alert-warning py-2 d-flex align-items-center gap-2">
                  <i className="bi bi-exclamation-triangle-fill"></i>
                  <strong>{voluntariosPendientes}</strong> voluntario(s) pendiente(s) de aprobación.
                </div>
              )}

              <div className="bo-table-wrapper">
                <table className="bo-table">
                  <thead>
                    <tr>
                      <th>RUT</th>
                      <th>Nombre</th>
                      <th>Email</th>
                      <th>Disponibilidad</th>
                      <th>Habilidades</th>
                      <th>Centros</th>
                      <th>Horas</th>
                      <th className="bo-actions-th">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(() => {
                      const filtrados = filtroVoluntarioCentro
                        ? voluntarios.filter((v) =>
                            (v.centros || []).some((c) => String(c.centro_id) === String(filtroVoluntarioCentro))
                          )
                        : voluntarios;
                      const ordenados = [...filtrados].sort((a, b) => {
                        const aPend = (a.centros || []).some((c) => c.estado === "pendiente") ? 0 : 1;
                        const bPend = (b.centros || []).some((c) => c.estado === "pendiente") ? 0 : 1;
                        return aPend - bPend;
                      });
                      return ordenados.length === 0 ? (
                        <tr><td colSpan="8" className="text-center text-muted py-4">No hay voluntarios registrados</td></tr>
                      ) : ordenados.map((v) => (
                        <tr key={v.id}>
                          <td><span className="bo-id">{v.rut ? `${v.rut.slice(0, -1)}-${v.rut.slice(-1)}` : ""}</span></td>
                          <td className="fw-medium">{v.nombre || "—"}</td>
                          <td>{v.email || "—"}</td>
                          <td className="text-capitalize">{v.disponibilidad?.replace("_", " ")}</td>
                          <td>
                            {(v.habilidades || []).length === 0 ? (
                              <span className="text-muted small">—</span>
                            ) : (
                              <div className="d-flex flex-wrap gap-1">
                                {v.habilidades.map((code) => {
                                  const hab = habilidadesVol.find((h) => h.code === code);
                                  return (
                                    <span key={code} className="badge bg-info text-dark small" title={hab?.descripcion || code}>
                                      {hab?.nombre || code}
                                    </span>
                                  );
                                })}
                              </div>
                            )}
                          </td>
                          <td>
                            {(v.centros || []).length === 0 ? (
                              <span className="text-muted small">—</span>
                            ) : (
                              <div className="d-flex flex-wrap gap-1">
                                {v.centros.map((vc) => {
                                  const cObj = centros.find((c) => String(c.id) === String(vc.centro_id));
                                  return (
                                    <span key={vc.id} className={`badge ${
                                      vc.estado === "activo" ? "bg-success" :
                                      vc.estado === "pendiente" ? "bg-warning text-dark" : "bg-secondary"
                                    } small`}>
                                      {cObj?.nombre || `Centro ${vc.centro_id}`}
                                      {vc.estado === "pendiente" && (
                                        <span className="ms-1">
                                          {(esAdmin || esEncargado) && (
                                            <>
                                              <i className="bi bi-check-lg cursor-pointer" style={{fontSize:11}}
                                                title="Aprobar"
                                                onClick={async () => {
                                                  await actualizarCentroVoluntario(vc.id, "activo");
                                                  setVoluntariosKey((k) => k + 1);
                                                }} />
                                              <i className="bi bi-x-lg cursor-pointer ms-1" style={{fontSize:11}}
                                                title="Rechazar"
                                                onClick={async () => {
                                                  if (window.confirm(`¿Rechazar asignación de ${v.nombre || v.rut} al centro?`)) {
                                                    await actualizarCentroVoluntario(vc.id, "inactivo");
                                                    setVoluntariosKey((k) => k + 1);
                                                  }
                                                }} />
                                            </>
                                          )}
                                        </span>
                                      )}
                                    </span>
                                  );
                                })}
                              </div>
                            )}
                          </td>
                          <td><span className="badge bg-accent">{v.horas_acumuladas || 0}h</span></td>
                          <td>
                            <div className="d-flex gap-1">
                              <button className="btn btn-sm btn-outline-primary py-0 px-1" title="Registrar horas"
                                onClick={async () => {
                                  setHorasVoluntario(v);
                                  setHorasForm({ horas: "", descripcion: "" });
                                  setHorasCentroSeleccionado("");
                                  const data = await getHorasVoluntario(v.id);
                                  setHorasData(data);
                                  setShowHorasModal(true);
                                }}>
                                <i className="bi bi-clock-history"></i>
                              </button>
                              <button className="btn btn-sm btn-outline-warning py-0 px-1" title="Notificar al voluntario"
                                onClick={() => {
                                  setNotifModal({ show: true, voluntario: v });
                                  setNotifForm({ titulo: "", mensaje: "" });
                                }}>
                                <i className="bi bi-bell"></i>
                              </button>
                              {esAdmin && (
                                <button className="btn btn-sm btn-outline-danger py-0 px-1" title="Eliminar"
                                  onClick={async () => {
                                    if (window.confirm(`¿Eliminar voluntario ${v.rut}?`)) {
                                      await eliminarVoluntario(v.id);
                                      setVoluntariosKey((k) => k + 1);
                                    }
                                  }}>
                                  <i className="bi bi-trash"></i>
                                </button>
                              )}
                            </div>
                          </td>
                        </tr>
                      ));
                    })()}
                  </tbody>
                </table>
              </div>

              {showHorasModal && horasVoluntario && (
                <div className="modal d-block modal-overlay" tabIndex="-1">
                  <div className="modal-dialog modal-dialog-centered">
                    <div className="modal-content">
                      <div className="modal-header">
                        <h5 className="modal-title">
                          <i className="bi bi-clock-history me-2 c-primary"></i>
                          Horas — {horasVoluntario.nombre || horasVoluntario.rut}
                        </h5>
                        <button type="button" className="btn-close" onClick={() => setShowHorasModal(false)} />
                      </div>
                      <div className="modal-body">
                        {horasData && (
                          <div className="mb-3">
                            <strong>Total acumulado: </strong>
                            <span className="badge bg-accent fs-6">{horasData.horas_acumuladas || 0}h</span>
                            {horasData.horas_por_centro && Object.keys(horasData.horas_por_centro).length > 0 && (
                              <div className="mt-1 d-flex flex-wrap gap-1">
                                {Object.entries(horasData.horas_por_centro).map(([cid, h]) => {
                                  const cObj = centros.find((c) => String(c.id) === String(cid));
                                  return (
                                    <span key={cid} className="badge bg-secondary small">
                                      {cObj?.nombre || `Centro ${cid}`}: {h}h
                                    </span>
                                  );
                                })}
                              </div>
                            )}
                            {horasData.registros?.length > 0 && (
                              <div className="mt-2">
                                <small className="text-muted">Registros anteriores:</small>
                                <ul className="list-unstyled mt-1">
                                  {horasData.registros.map((r) => {
                                    const cObj = centros.find((c) => String(c.id) === String(r.centro_id));
                                    return (
                                      <li key={r.id} className="small border-bottom py-1">
                                        <strong>{r.horas}h</strong> — {r.descripcion || "Sin descripción"}
                                        {r.centro_id && (
                                          <span className="badge bg-light text-dark ms-1" style={{fontSize:10}}>
                                            {cObj?.nombre || `Centro ${r.centro_id}`}
                                          </span>
                                        )}
                                        <span className="text-muted ms-2">({new Date(r.fecha).toLocaleDateString("es-CL")})</span>
                                      </li>
                                    );
                                  })}
                                </ul>
                              </div>
                            )}
                          </div>
                        )}
                        <hr />
                        <h6>Registrar horas</h6>
                        <div className="mb-2">
                          <label className="form-label">Centro</label>
                          <select className="form-select form-select-sm"
                            value={horasCentroSeleccionado}
                            onChange={(e) => setHorasCentroSeleccionado(e.target.value)}>
                            <option value="">Seleccionar centro...</option>
                            {(horasVoluntario.centros || [])
                              .filter((c) => c.estado === "activo")
                              .map((vc) => {
                                const cObj = centros.find((c) => String(c.id) === String(vc.centro_id));
                                return (
                                  <option key={vc.id} value={vc.centro_id}>
                                    {cObj?.nombre || `Centro ${vc.centro_id}`}
                                  </option>
                                );
                              })}
                          </select>
                        </div>
                        <div className="mb-2">
                          <label className="form-label">Horas</label>
                          <input type="number" className="form-control" min="1" max="24"
                            value={horasForm.horas}
                            onChange={(e) => setHorasForm({ ...horasForm, horas: e.target.value })} />
                        </div>
                        <div className="mb-2">
                          <label className="form-label">Descripción</label>
                          <textarea className="form-control" rows="2"
                            value={horasForm.descripcion}
                            onChange={(e) => setHorasForm({ ...horasForm, descripcion: e.target.value })} />
                        </div>
                      </div>
                      <div className="modal-footer">
                        <button className="btn btn-secondary" onClick={() => setShowHorasModal(false)}>Cerrar</button>
                        <button className="btn btn-accent"
                          disabled={!horasCentroSeleccionado || !horasForm.horas || parseInt(horasForm.horas) <= 0}
                          onClick={async () => {
                            await registrarHorasVoluntario(horasVoluntario.id, parseInt(horasForm.horas), horasForm.descripcion, horasCentroSeleccionado);
                            const data = await getHorasVoluntario(horasVoluntario.id);
                            setHorasData(data);
                            setHorasForm({ horas: "", descripcion: "" });
                            setVoluntariosKey((k) => k + 1);
                          }}>
                          <i className="bi bi-save me-1"></i>Guardar horas
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {notifModal.show && notifModal.voluntario && (
                <div className="modal d-block modal-overlay" tabIndex="-1">
                  <div className="modal-dialog modal-dialog-centered">
                    <div className="modal-content">
                      <div className="modal-header">
                        <h5 className="modal-title">
                          <i className="bi bi-bell me-2 c-primary"></i>
                          Notificar — {notifModal.voluntario.nombre || notifModal.voluntario.rut}
                        </h5>
                        <button type="button" className="btn-close" onClick={() => setNotifModal({ show: false, voluntario: null })} />
                      </div>
                      <div className="modal-body">
                        <div className="mb-2">
                          <label className="form-label fw-semibold">Título</label>
                          <input type="text" className="form-control"
                            placeholder="Ej: Se requiere tu ayuda en el centro"
                            value={notifForm.titulo}
                            onChange={(e) => setNotifForm({ ...notifForm, titulo: e.target.value })} />
                        </div>
                        <div className="mb-2">
                          <label className="form-label fw-semibold">Mensaje</label>
                          <textarea className="form-control" rows="3"
                            placeholder="Describe por qué se necesita al voluntario..."
                            value={notifForm.mensaje}
                            onChange={(e) => setNotifForm({ ...notifForm, mensaje: e.target.value })} />
                        </div>
                      </div>
                      <div className="modal-footer">
                        <button className="btn btn-secondary" onClick={() => setNotifModal({ show: false, voluntario: null })}>Cancelar</button>
                        <button className="btn btn-warning"
                          disabled={!notifForm.titulo.trim() || !notifForm.mensaje.trim() || notifEnviando}
                          onClick={async () => {
                            setNotifEnviando(true);
                            try {
                              await enviarNotificacion({
                                voluntario_id: notifModal.voluntario.id,
                                titulo: notifForm.titulo.trim(),
                                mensaje: notifForm.mensaje.trim(),
                              });
                              setNotifModal({ show: false, voluntario: null });
                            } catch (err) {
                              alert(err?.response?.data?.error || "Error al enviar notificación");
                            } finally {
                              setNotifEnviando(false);
                            }
                          }}>
                          {notifEnviando ? <><span className="spinner-border spinner-border-sm me-1" /> Enviando...</> : <><i className="bi bi-send me-1"></i>Enviar</>}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

            </>
          )}

          {/* USUARIOS (solo admin) */}
          {activeTab === "usuarios" && (
            <>
              <div className="d-flex justify-content-between align-items-center mb-4">
                <h2 className="m-0 c-heading">
                  <i className="bi bi-people-fill me-2 c-primary"></i>Usuarios
                </h2>
              </div>

              <div className="bo-table-wrapper">
                <table className="bo-table">
                  <thead>
                    <tr>
                      <th>RUT</th>
                      <th>Nombre</th>
                      <th>Email</th>
                      <th>Rol</th>
                      <th>Centro asignado</th>
                    </tr>
                  </thead>
                  <tbody>
                    {usuarios.map((u) => {
                      const esAdmin = u.rol === "admin";
                      return (
                        <tr key={u.rut}>
                          <td><span className="bo-id">{u.rut ? `${u.rut.slice(0, -1)}-${u.rut.slice(-1)}` : ""}</span></td>
                          <td className="fw-medium">{u.nombre}</td>
                          <td>{u.email}</td>
                          <td>
                            <select className="form-select form-select-sm"
                              value={u.rol}
                              onChange={async (e) => {
                                const newRol = e.target.value;
                                if (newRol === "admin") {
                                  await actualizarUsuario(u.rut, { is_staff: true, centro_acopio_id: null });
                                } else if (newRol === "encargado") {
                                  await actualizarUsuario(u.rut, { is_staff: false });
                                } else {
                                  await actualizarUsuario(u.rut, { is_staff: false, centro_acopio_id: null });
                                }
                                setUsuariosKey((k) => k + 1);
                              }}>
                              <option value="donante">Donante</option>
                              <option value="encargado">Encargado</option>
                              <option value="admin">Administrador</option>
                            </select>
                          </td>
                          <td>
                            {esAdmin ? (
                              <span className="c-muted small">—</span>
                            ) : (
                              <select className="form-select form-select-sm"
                                value={u.centro_acopio_id || ""}
                                onChange={async (e) => {
                                  await actualizarUsuario(u.rut, { centro_acopio_id: e.target.value || null });
                                  setUsuariosKey((k) => k + 1);
                                }}>
                                <option value="">Sin centro</option>
                                {centros.map((c) => (
                                  <option key={c.id} value={c.id}>{c.nombre}</option>
                                ))}
                              </select>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </>
          )}

        </main>
      </div>

      {/* ── CRUD MODAL ── */}
      {showModal && (
        <div className="modal d-block modal-overlay" tabIndex="-1">
          <div className="modal-dialog modal-lg modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  <i className={`bi ${editItem ? "bi-pencil" : "bi-plus-lg"} me-2 c-primary`}></i>
                  {editItem ? `Editar ${modalEntity}` : `Crear ${modalEntity}`}
                </h5>
                <button type="button" className="btn-close" onClick={closeModal}></button>
              </div>
              <form onSubmit={handleSave}>
                <div className="modal-body">
                  <div className="row g-3">
                    {modalEntity === "donacion" && (
                      <>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Tipo</label>
                          {editItem ? (
                            <input name="tipo" className={`form-control${formErrors.tipo ? " is-invalid" : ""}`} value={form.tipo || ""} onChange={handleFormChange} />
                          ) : (
                            <select name="tipo" className={`form-select${formErrors.tipo ? " is-invalid" : ""}`} value={form.tipo || ""} onChange={handleFormChange}>
                              <option value="">Selecciona...</option>
                              {["Alimentos no perecibles", "Ropa y abrigo", "Insumos médicos", "Artículos de higiene", "Donación Monetaria", "Utensilios del hogar", "Otros"].map((t) => <option key={t} value={t}>{t}</option>)}
                            </select>
                          )}
                          {form.tipo === "Otros" && !editItem && (
                            <input name="tipoPersonalizado" className="form-control mt-2" placeholder="Describe el tipo..." value={form.tipoPersonalizado || ""} onChange={handleFormChange} />
                          )}
                          {formErrors.tipo && <div className="invalid-feedback d-block">{formErrors.tipo}</div>}
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Cantidad</label>
                          <input name="cantidad" type="number" className={`form-control${formErrors.cantidad ? " is-invalid" : ""}`} value={form.cantidad || ""} onChange={handleFormChange} />
                          {formErrors.cantidad && <div className="invalid-feedback d-block">{formErrors.cantidad}</div>}
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Unidad</label>
                          <input name="unidad" className={`form-control${formErrors.unidad ? " is-invalid" : ""}`} value={form.unidad || ""} onChange={handleFormChange} />
                          {formErrors.unidad && <div className="invalid-feedback d-block">{formErrors.unidad}</div>}
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Origen</label>
                          <input name="origen" className={`form-control${formErrors.origen ? " is-invalid" : ""}`} value={formatearRut(form.origen || "")} onChange={(e) => { const raw = limpiarRut(e.target.value); setForm({ ...form, origen: raw }); if (formErrors.origen) setFormErrors({ ...formErrors, origen: "" }); }} />
                          {formErrors.origen && <div className="invalid-feedback d-block">{formErrors.origen}</div>}
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Centro</label>
                          <select name="centroId" className={`form-select${formErrors.centroId ? " is-invalid" : ""}`} value={form.centroId || ""} onChange={handleFormChange}>
                            <option value="">Selecciona...</option>
                            {centros.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                          </select>
                          {formErrors.centroId && <div className="invalid-feedback d-block">{formErrors.centroId}</div>}
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Estado</label>
                          <select name="estado" className="form-select" value={form.estado || "Donación Registrada"} onChange={handleFormChange}>
                            {estadosDonacion.map((est) => <option key={est} value={est}>{est}</option>)}
                          </select>
                        </div>
                      </>
                    )}
                    {modalEntity === "necesidad" && (
                      <>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Recurso</label>
                          <input name="recurso" className={`form-control${formErrors.recurso ? " is-invalid" : ""}`} value={form.recurso || ""} onChange={handleFormChange} />
                          {formErrors.recurso && <div className="invalid-feedback d-block">{formErrors.recurso}</div>}
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Cantidad</label>
                          <input name="cantidad" type="number" className={`form-control${formErrors.cantidad ? " is-invalid" : ""}`} value={form.cantidad || ""} onChange={handleFormChange} />
                          {formErrors.cantidad && <div className="invalid-feedback d-block">{formErrors.cantidad}</div>}
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Unidad</label>
                          <input name="unidad" className={`form-control${formErrors.unidad ? " is-invalid" : ""}`} value={form.unidad || ""} onChange={handleFormChange} />
                          {formErrors.unidad && <div className="invalid-feedback d-block">{formErrors.unidad}</div>}
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Centro destino</label>
                          <select name="centroId" className={`form-select${formErrors.centroId ? " is-invalid" : ""}`} value={form.centroId || ""} onChange={handleFormChange}>
                            <option value="">Selecciona...</option>
                            {centros.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
                          </select>
                          {formErrors.centroId && <div className="invalid-feedback d-block">{formErrors.centroId}</div>}
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Urgencia</label>
                          <select name="urgencia" className="form-select" value={form.urgencia || "Media"} onChange={handleFormChange}>
                            {urgencias.map((u) => <option key={u} value={u}>{u}</option>)}
                          </select>
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Estado</label>
                          <select name="estado" className="form-select" value={form.estado || "Pendiente"} onChange={handleFormChange}>
                            <option value="Pendiente">Pendiente</option>
                            <option value="Activa">Activa</option>
                            <option value="Cubierta">Cubierta</option>
                          </select>
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Reportado por</label>
                          <input name="reportadoPor" className={`form-control${formErrors.reportadoPor ? " is-invalid" : ""}`} value={form.reportadoPor || ""} onChange={handleFormChange} />
                          {formErrors.reportadoPor && <div className="invalid-feedback d-block">{formErrors.reportadoPor}</div>}
                        </div>
                        <div className="col-12">
                          <label className="form-label small fw-semibold">Descripción</label>
                          <RichTextEditor content={form.descripcion || ""} onChange={(value) => setForm({ ...form, descripcion: value })} placeholder="Describe la necesidad en detalle..." />
                        </div>
                      </>
                    )}
                    {modalEntity === "centro" && (
                      <>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Nombre</label>
                          <input name="nombre" className={`form-control${formErrors.nombre ? " is-invalid" : ""}`} value={form.nombre || ""} onChange={handleFormChange} />
                          {formErrors.nombre && <div className="invalid-feedback d-block">{formErrors.nombre}</div>}
                        </div>
                        <div className="col-md-6">
                          <SelectRegion value={form.region} onChange={handleFormChange} error={formErrors.region} />
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Teléfono</label>
                          <input name="telefono" className="form-control" value={form.telefono || ""} onChange={handleFormChange} placeholder="+56 9 XXXX XXXX" />
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Encargado</label>
                          <input name="encargado" className={`form-control${formErrors.encargado ? " is-invalid" : ""}`} value={form.encargado || ""} onChange={handleFormChange} />
                          {formErrors.encargado && <div className="invalid-feedback d-block">{formErrors.encargado}</div>}
                        </div>
                        <div className="col-12">
                          <AddressPicker
                            label="Dirección (búsqueda + mapa)"
                            initialLocation={form.latitud && form.longitud ? { lat: parseFloat(form.latitud), lng: parseFloat(form.longitud) } : null}
                            onLocationChange={({ lat, lng }) => setForm({ ...form, latitud: lat.toString(), longitud: lng.toString() })}
                          />
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Capacidad total</label>
                          <input name="capacidadTotal" type="number" className={`form-control${formErrors.capacidadTotal ? " is-invalid" : ""}`} value={form.capacidadTotal || ""} onChange={handleFormChange} />
                          {formErrors.capacidadTotal && <div className="invalid-feedback d-block">{formErrors.capacidadTotal}</div>}
                        </div>
                        <div className="col-md-3">
                          <label className="form-label small fw-semibold">Capacidad usada</label>
                          <input name="capacidadUsada" type="number" className={`form-control${formErrors.capacidadUsada ? " is-invalid" : ""}`} value={form.capacidadUsada ?? ""} onChange={handleFormChange} />
                          {formErrors.capacidadUsada && <div className="invalid-feedback d-block">{formErrors.capacidadUsada}</div>}
                        </div>
                        <div className="col-md-6">
                          <label className="form-label small fw-semibold">Estado</label>
                          <select name="estado" className="form-select" value={form.estado || "Activo"} onChange={handleFormChange}>
                            <option value="Activo">Activo</option>
                            <option value="Inactivo">Inactivo</option>
                          </select>
                        </div>
                      </>
                    )}
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={closeModal}>Cancelar</button>
                  <button type="submit" className="btn btn-primary">
                    <i className="bi bi-check-lg me-1"></i>{editItem ? "Guardar cambios" : "Crear"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      { /* ── AGRADECIMIENTO MODAL ── */ }
      {showAgradecerModal && agradecerDonacion && (
        <div className="modal d-block modal-overlay" tabIndex="-1">
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  <i className="bi bi-heart-fill me-2 c-danger"></i>Agradecer a donante
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowAgradecerModal(false)}></button>
              </div>
              <div className="modal-body">
                <p className="small c-muted mb-2">
                  Donaci&oacute;n #{agradecerDonacion.id} de <strong>{agradecerDonacion.origen}</strong>
                  {" — "}{agradecerDonacion.tipo} x{agradecerDonacion.cantidad} {agradecerDonacion.unidad}
                </p>
                <label className="form-label small fw-semibold">Mensaje de agradecimiento</label>
                <textarea
                  className="form-control"
                  rows={4}
                  value={agradecerMensaje}
                  onChange={(e) => setAgradecerMensaje(e.target.value)}
                  placeholder="Escribe un mensaje para agradecer al donante..."
                />
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setShowAgradecerModal(false)}>Cancelar</button>
                <button type="button" className="btn btn-danger"
                  disabled={!agradecerMensaje.trim() || agradecerEnviando}
                  onClick={async () => {
                    setAgradecerEnviando(true);
                    try {
                      await crearAgradecimiento({
                        centro_id: agradecerDonacion.centroId,
                        usuario_rut: agradecerDonacion.origen,
                        donacion_id: agradecerDonacion.id,
                        mensaje: agradecerMensaje.trim(),
                      });
                      setShowAgradecerModal(false);
                      alert("¡Agradecimiento enviado!");
                    } catch {
                      alert("Error al enviar agradecimiento");
                    } finally {
                      setAgradecerEnviando(false);
                    }
                  }}>
                  {agradecerEnviando ? "Enviando..." : <><i className="bi bi-send me-1"></i>Enviar</>}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
