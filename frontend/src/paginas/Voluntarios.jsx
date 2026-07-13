import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../componentes/AuthContext";
import {
  getMiPerfilVoluntario, crearVoluntario, actualizarVoluntario,
  getHabilidadesVoluntario, getVoluntarioCentros, solicitarCentroVoluntario,
  getNotificacionesVoluntario, marcarNotificacionLeida,
  getNecesidades, getCentros,
} from "../api.js";
import { validarRequerido, validarForm } from "../componentes/Validaciones.js";

const DISPONIBILIDAD_OPTS = [
  { value: "diaria", label: "Diaria" },
  { value: "semanal", label: "Semanal" },
  { value: "fines_semana", label: "Fines de semana" },
  { value: "emergencia", label: "Solo emergencias" },
];

const URGENCIA_BADGE = {
  Alta: "bg-danger",
  Media: "bg-warning text-dark",
  Baja: "bg-success",
};

const ESTADO_BADGE = {
  activo: "bg-success",
  pendiente: "bg-warning text-dark",
  inactivo: "bg-secondary",
};

export default function Voluntarios() {
  const { isAuth, user } = useAuth();
  const navigate = useNavigate();

  const [perfil, setPerfil] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [habilidades, setHabilidades] = useState([]);
  const [oportunidades, setOportunidades] = useState([]);
  const [centros, setCentros] = useState([]);
  const [misCentros, setMisCentros] = useState([]);
  const [notificaciones, setNotificaciones] = useState([]);
  const [showNotifModal, setShowNotifModal] = useState(false);

  const [form, setForm] = useState({
    disponibilidad: "emergencia",
    habilidades: [],
    centro_id: "",
  });
  const [formError, setFormError] = useState("");
  const [formErrors, setFormErrors] = useState({});
  const [guardando, setGuardando] = useState(false);
  const [exito, setExito] = useState("");
  const [solicitandoCentro, setSolicitandoCentro] = useState(null);
  const [centroDropdown, setCentroDropdown] = useState(false);
  const [centroFiltro, setCentroFiltro] = useState("");
  const centroRef = useRef(null);

  useEffect(() => {
    getHabilidadesVoluntario().then(setHabilidades);
    getCentros().then(setCentros);
    getNecesidades().then((todas) => {
      const voluntariado = (Array.isArray(todas) ? todas : [])
        .filter((n) => n.categoria === "VOLUNTARIADO" && n.estado === "Activa");
      setOportunidades(voluntariado);
    });
  }, []);

  useEffect(() => {
    function handleClickOutside(e) {
      if (centroRef.current && !centroRef.current.contains(e.target)) {
        setCentroDropdown(false);
        setCentroFiltro("");
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const loadCentros = (perfilData) => {
    if (perfilData?.id) {
      getVoluntarioCentros(perfilData.id).then(setMisCentros);
    }
  };

  const loadNotificaciones = (perfilData) => {
    if (perfilData?.id) {
      getNotificacionesVoluntario(perfilData.id).then(setNotificaciones);
    }
  };

  useEffect(() => {
    if (!isAuth) {
      setCargando(false);
      return;
    }
    getMiPerfilVoluntario().then((p) => {
      setPerfil(p);
      if (p) {
        setForm({
          disponibilidad: p.disponibilidad || "emergencia",
          habilidades: p.habilidades || [],
        });
        loadCentros(p);
        loadNotificaciones(p);
      }
      setCargando(false);
    });
  }, [isAuth]);

  const toggleHabilidad = (code) => {
    setForm((prev) => ({
      ...prev,
      habilidades: prev.habilidades.includes(code)
        ? prev.habilidades.filter((h) => h !== code)
        : [...prev.habilidades, code],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError("");
    setExito("");

    const errores = {};
    if (!form.habilidades.length) {
      errores.habilidades = "Selecciona al menos una habilidad";
    }
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;

    setGuardando(true);
    try {
      if (perfil) {
        await actualizarVoluntario(perfil.id, { disponibilidad: form.disponibilidad, habilidades: form.habilidades });
        setExito("Perfil de voluntario actualizado correctamente.");
      } else {
        const payload = { disponibilidad: form.disponibilidad, habilidades: form.habilidades };
        if (form.centro_id) payload.centro_id = form.centro_id;
        await crearVoluntario(payload);
        setExito("Solicitud enviada. Un administrador revisará tu inscripción y te activará pronto.");
      }
      const actualizado = await getMiPerfilVoluntario();
      setPerfil(actualizado);
      if (actualizado) {
        loadCentros(actualizado);
        loadNotificaciones(actualizado);
      }
    } catch (err) {
      setFormError(err?.response?.data?.error || "Error al guardar el perfil de voluntario.");
    } finally {
      setGuardando(false);
    }
  };

  const handleSolicitarCentro = async (centroId) => {
    setSolicitandoCentro(centroId);
    try {
      await solicitarCentroVoluntario(perfil.id, centroId);
      setExito("Solicitud de centro enviada. Espera aprobación del administrador.");
      loadCentros(perfil);
    } catch (err) {
      const msg = err?.response?.data?.error || "Error al solicitar centro";
      setFormError(msg);
    } finally {
      setSolicitandoCentro(null);
      setCentroDropdown(false);
      setCentroFiltro("");
    }
  };

  const centrosAsignados = misCentros.map((c) => c.centro_id);
  const centrosDisponibles = centros.filter((c) => !centrosAsignados.includes(String(c.id)) && !centrosAsignados.includes(c.id));

  if (cargando) {
    return <div className="container mt-5 text-center"><div className="spinner-border" /></div>;
  }

  return (
    <div className="voluntarios">
      <div className="content-surface">
        <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
          <div>
            <h1 className="fw-bold mb-1">Voluntarios</h1>
            <p className="m-0 c-muted">Únete como voluntario y ayuda a coordinar la ayuda humanitaria en terreno.</p>
          </div>
          <span className="page-header-pill accent-pill">
            <i className="bi bi-people-fill"></i> Voluntariado
          </span>
        </div>

        {exito && (
          <div className="alert alert-success alert-dismissible fade show">
            {exito}
            <button type="button" className="btn-close" onClick={() => setExito("")} />
          </div>
        )}

        {!isAuth ? (
          <div className="p-5 rounded-4 card-surface text-center">
            <i className="bi bi-person-circle icon-lg c-primary d-block mb-3"></i>
            <h3 className="mt-3">Inicia sesión para ser voluntario</h3>
            <p className="c-muted">Debes tener una cuenta registrada para inscribirte como voluntario.</p>
            <button className="btn btn-primary btn-lg me-2" onClick={() => navigate("/login")}>
              Iniciar sesión
            </button>
            <button className="btn btn-outline-primary btn-lg" onClick={() => navigate("/registro")}>
              Crear cuenta
            </button>
          </div>
        ) : (
          <div className="row g-4">
            {/* ── Columna izquierda: formulario ── */}
            <div className="col-12 col-lg-7">
              <div className="p-4 rounded-4 card-surface">
                <h2 className="fw-bold fs-5 mb-3 c-heading">
                  <i className="bi bi-person-fill me-2 c-primary"></i>
                  {perfil ? "Mi perfil de voluntario" : "Regístrate como voluntario"}
                </h2>

                {formError && <div className="alert alert-danger py-2">{formError}</div>}

                <div className="d-flex align-items-center gap-3 mb-3 p-2 rounded-3 small bg-page">
                  <div>
                    <span className="fw-semibold c-heading">RUT:</span>{" "}
                    <span className="c-muted">{user?.rut}</span>
                  </div>
                </div>

                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label fw-semibold small">Disponibilidad</label>
                    <select
                      className="form-select"
                      value={form.disponibilidad}
                      onChange={(e) => setForm({ ...form, disponibilidad: e.target.value })}
                    >
                      {DISPONIBILIDAD_OPTS.map((o) => (
                        <option key={o.value} value={o.value}>{o.label}</option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-3">
                    <label className="form-label fw-semibold small">Habilidades</label>
                    <div className="row g-2">
                      {habilidades.map((h) => (
                        <div key={h.code} className="col-md-4 col-sm-6 d-flex">
                          <div
                            className={`volunteer-skill-card p-2 rounded border cursor-pointer w-100 d-flex flex-column ${
                              form.habilidades.includes(h.code) ? "border-accent bg-accent-light" : ""
                            }`}
                            onClick={() => toggleHabilidad(h.code)}
                          >
                            <span className="fw-semibold small">{h.nombre}</span>
                            <small className="text-muted skill-desc">{h.descripcion}</small>
                          </div>
                        </div>
                      ))}
                    </div>
                    {formErrors.habilidades && <div className="text-danger small mt-1">{formErrors.habilidades}</div>}
                  </div>

                  {!perfil && (
                    <div className="mb-3 position-relative" ref={centroRef}>
                      <label className="form-label fw-semibold small">Centro de acopio <span className="c-muted fw-normal">(opcional)</span></label>
                      <input
                        type="text"
                        className="form-control"
                        placeholder="Escribe para buscar un centro..."
                        autoComplete="off"
                        value={centroDropdown ? centroFiltro : centros.find((c) => String(c.id) === form.centro_id)?.nombre || ""}
                        onFocus={() => { setCentroDropdown(true); setCentroFiltro(""); }}
                        onChange={(e) => { setCentroFiltro(e.target.value); setCentroDropdown(true); }}
                      />
                      {centroDropdown && (
                        <ul className="list-group position-absolute w-100 shadow-sm dropdown-scrollable" style={{ zIndex: 20 }}>
                          <li
                            className={`list-group-item list-group-item-action small cursor-pointer ${form.centro_id === "" ? "active" : ""}`}
                            onClick={() => { setForm({ ...form, centro_id: "" }); setCentroDropdown(false); setCentroFiltro(""); }}
                          >
                            Sin centro específico
                          </li>
                          {centros.filter((c) => c.nombre.toLowerCase().includes(centroFiltro.toLowerCase())).map((c) => (
                            <li
                              key={c.id}
                              className={`list-group-item list-group-item-action small cursor-pointer ${String(form.centro_id) === String(c.id) ? "active" : ""}`}
                              onClick={() => { setForm({ ...form, centro_id: String(c.id) }); setCentroDropdown(false); setCentroFiltro(""); }}
                            >
                              <i className="bi bi-geo-alt me-1 text-muted"></i>{c.nombre}
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  )}

                  <button type="submit" className="btn btn-primary w-100" disabled={guardando}>
                    {guardando ? (
                      <><span className="spinner-border spinner-border-sm me-1" /> Guardando...</>
                    ) : (
                      <><i className="bi bi-send-fill me-2"></i>{perfil ? "Actualizar perfil" : "Registrarme como voluntario"}</>
                    )}
                  </button>
                </form>
              </div>

              {/* ── Mis centros ── */}
              {perfil && (
                <div className="p-4 rounded-4 card-surface mt-4">
                  <h2 className="fw-bold fs-5 mb-3 c-heading">
                    <i className="bi bi-building me-2 c-primary"></i>Mis centros
                  </h2>

                  {misCentros.length === 0 ? (
                    <div className="text-center py-3">
                      <i className="bi bi-geo-alt icon-lg c-muted d-block mb-2"></i>
                      <p className="c-muted mb-2">Aún no estás asignado a ningún centro.</p>
                      <p className="c-muted small mb-0">Selecciona un centro de la lista para solicitar tu incorporación.</p>
                    </div>
                  ) : (
                    <div className="d-flex flex-column gap-2 mb-3">
                      {misCentros.map((mc) => {
                        const centro = centros.find((c) => String(c.id) === String(mc.centro_id));
                        return (
                          <div key={mc.id} className="d-flex align-items-center justify-content-between p-2 rounded-3 bg-page">
                            <div>
                              <span className="fw-semibold small">
                                <i className="bi bi-geo-alt me-1 text-muted"></i>
                                {centro?.nombre || `Centro ${mc.centro_id}`}
                              </span>
                            </div>
                            <span className={`badge ${ESTADO_BADGE[mc.estado] || "bg-secondary"} small`}>
                              {mc.estado === "activo" ? "Activo" : mc.estado === "pendiente" ? "Pendiente" : "Inactivo"}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  )}

                  <div className="position-relative" ref={centroRef}>
                    <button
                      className="btn btn-outline-primary btn-sm w-100"
                      onClick={() => setCentroDropdown(!centroDropdown)}
                      disabled={centrosDisponibles.length === 0}
                    >
                      <i className="bi bi-plus-lg me-1"></i>
                      {centrosDisponibles.length === 0 ? "Todos los centros asignados" : "Solicitar nuevo centro"}
                    </button>
                    {centroDropdown && centrosDisponibles.length > 0 && (
                      <div className="mt-2">
                        <input
                          type="text"
                          className="form-control form-control-sm mb-1"
                          placeholder="Buscar centro..."
                          autoFocus
                          value={centroFiltro}
                          onChange={(e) => setCentroFiltro(e.target.value)}
                        />
                        <ul className="list-group dropdown-scrollable" style={{ maxHeight: 200, overflow: "auto" }}>
                          {centrosDisponibles.filter((c) =>
                            c.nombre.toLowerCase().includes(centroFiltro.toLowerCase())
                          ).map((c) => (
                            <li
                              key={c.id}
                              className="list-group-item list-group-item-action small cursor-pointer"
                              onClick={() => handleSolicitarCentro(String(c.id))}
                            >
                              <i className="bi bi-geo-alt me-1 text-muted"></i>{c.nombre}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* ── Columna derecha: resumen + oportunidades ── */}
            <div className="col-12 col-lg-5">
              {perfil && (
                <div className="p-4 rounded-4 card-surface text-center mb-4">
                  <div className="d-flex justify-content-between align-items-center mb-3">
                    <h2 className="fw-bold fs-5 mb-0 c-heading">
                      <i className="bi bi-clock-history me-2 c-primary"></i>Horas registradas
                    </h2>
                    <button
                      className="btn btn-sm btn-outline-primary position-relative"
                      onClick={() => setShowNotifModal(true)}
                    >
                      <i className="bi bi-bell-fill"></i>
                      {notificaciones.filter((n) => !n.leida).length > 0 && (
                        <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style={{fontSize:10}}>
                          {notificaciones.filter((n) => !n.leida).length}
                        </span>
                      )}
                    </button>
                  </div>
                  <span className="display-4 fw-bold c-primary">
                    {perfil.horas_acumuladas || 0}
                  </span>
                  <span className="h4 ms-2 c-muted">horas</span>
                  <p className="c-muted mt-2 small mb-0">Total acumulado como voluntario</p>
                </div>
              )}

              <div className="p-4 rounded-4 card-surface">
                <h2 className="fw-bold fs-5 mb-3 c-heading">
                  <i className="bi bi-megaphone-fill me-2 c-primary"></i>Oportunidades
                </h2>
                {oportunidades.length === 0 ? (
                  <p className="c-muted small mb-0">No hay oportunidades de voluntariado disponibles en este momento.</p>
                ) : (
                  <div className="d-flex flex-column gap-2">
                    {oportunidades.map((op) => (
                      <div key={op.id} className="p-3 rounded-3 bg-page">
                        <div className="d-flex w-100 justify-content-between align-items-start mb-1">
                          <h6 className="mb-0 fw-semibold">{op.recurso}</h6>
                          <span className={`badge ${URGENCIA_BADGE[op.urgencia] || "bg-secondary"} badge-xs`}>
                            {op.urgencia}
                          </span>
                        </div>
                        <p className="mb-1 c-muted small">{op.descripcion}</p>
                        <small className="c-muted"><i className="bi bi-geo-alt me-1"></i>{op.centro}</small>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Modal Notificaciones ── */}
      {showNotifModal && (
        <div className="modal fade show d-block" tabIndex={-1} style={{backgroundColor: "rgba(0,0,0,0.5)"}}
          onClick={() => setShowNotifModal(false)}>
          <div className="modal-dialog modal-dialog-centered" onClick={(e) => e.stopPropagation()}>
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title fw-bold">
                  <i className="bi bi-bell-fill me-2 c-primary"></i>Mis notificaciones
                  {notificaciones.filter((n) => !n.leida).length > 0 && (
                    <span className="badge bg-danger ms-2" style={{fontSize:12}}>
                      {notificaciones.filter((n) => !n.leida).length} nuevas
                    </span>
                  )}
                </h5>
                <button type="button" className="btn-close" onClick={() => setShowNotifModal(false)}></button>
              </div>
              <div className="modal-body" style={{maxHeight: "60vh", overflowY: "auto"}}>
                {notificaciones.length === 0 ? (
                  <div className="text-center py-4">
                    <i className="bi bi-bell-slash icon-lg c-muted d-block mb-2"></i>
                    <p className="c-muted mb-0">No tienes notificaciones.</p>
                  </div>
                ) : (
                  <div className="d-flex flex-column gap-2">
                    {notificaciones.map((n) => (
                      <div key={n.id}
                        className={`p-3 rounded-3 ${n.leida ? "bg-page" : "bg-light border-start border-primary border-3"}`}
                        style={{cursor: "pointer"}}
                        onClick={async () => {
                          if (!n.leida) {
                            await marcarNotificacionLeida(n.id);
                            loadNotificaciones(perfil);
                          }
                        }}>
                        <div className="d-flex w-100 justify-content-between align-items-start mb-1">
                          <h6 className="mb-0 fw-semibold small">{n.titulo}</h6>
                          {!n.leida && <span className="badge bg-primary" style={{fontSize:9}}>NUEVA</span>}
                        </div>
                        <p className="mb-1 c-muted small">{n.mensaje}</p>
                        <small className="text-muted">
                          <i className="bi bi-clock me-1"></i>
                          {new Date(n.fecha_creacion).toLocaleDateString("es-CL")}
                        </small>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
