import { useState, useEffect, useRef } from "react";
import { Navigate, Link } from "react-router-dom";
import { useAuth } from "../componentes/AuthContext";
import { getDonaciones, actualizarCuenta, getLogros, getMisLogros, getMisAgradecimientos, getCentrosSeguidos } from "../api.js";
import api from "../servicios/api.js";
import { validarRequerido, validarEmail, validarForm } from "../componentes/Validaciones.js";
import LogrosModal from "../componentes/LogrosModal.jsx";

export default function Perfil() {
  const { user, isAuth, updateUser } = useAuth();
  const [donaciones, setDonaciones] = useState([]);
  const [editando, setEditando] = useState(false);
  const [guardado, setGuardado] = useState(false);
  const guardadoTimer = useRef(null);
  const [logros, setLogros] = useState([]);
  const [todosLogros, setTodosLogros] = useState([]);
  const [showLogrosModal, setShowLogrosModal] = useState(false);
  const [agradecimientos, setAgradecimientos] = useState([]);
  const [seguidos, setSeguidos] = useState([]);

  const [form, setForm] = useState({ nombre: "", email: "" });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    if (!isAuth) return;
    getDonaciones().then((lista) => setDonaciones(lista.reverse()));
    getLogros().then(setTodosLogros);
    getMisLogros().then(setLogros);
    getMisAgradecimientos().then(setAgradecimientos);
    getCentrosSeguidos().then(setSeguidos);
  }, [isAuth, user?.rut]);

  useEffect(() => {
    if (editando) setForm({ nombre: user.nombre || "", email: user.email || "" });
  }, [editando, user?.nombre, user?.email]);

  useEffect(() => {
    return () => clearTimeout(guardadoTimer.current);
  }, []);

  if (!isAuth) return <Navigate to="/login" replace />;

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (formErrors[e.target.name]) setFormErrors({ ...formErrors, [e.target.name]: "" });
  };

  const handleSave = async (e) => {
    e.preventDefault();
    const reglas = [
      { campo: "nombre", nombre: "Nombre", validaciones: [validarRequerido] },
      { campo: "email", nombre: "Correo electrónico", validaciones: [validarRequerido, validarEmail] },
    ];
    const errores = validarForm(form, reglas);
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;
    try {
      await actualizarCuenta(user.rut, { nombre: form.nombre, email: form.email });
      updateUser({ nombre: form.nombre, email: form.email });
      setGuardado(true);
      setEditando(false);
      clearTimeout(guardadoTimer.current);
      guardadoTimer.current = setTimeout(() => setGuardado(false), 3000);
    } catch {
      setFormErrors({ general: "Error al guardar" });
    }
  };

  const estadoBadge = (est) => {
    const map = { "Entregado": "bg-success", "En tránsito": "bg-info text-dark", "En acopio": "bg-warning text-dark" };
    return <span className={`badge ${map[est] || "bg-secondary"}`}>{est}</span>;
  };

  const totalDonado = donaciones.reduce((acc, d) => acc + (parseFloat(d.cantidad) || 0), 0);
  const centrosUnicos = new Set(donaciones.map((d) => d.centroId)).size;
  const monetarioTotal = donaciones.filter((d) => d.tipo === "Donación Monetaria").reduce((acc, d) => acc + (parseFloat(d.cantidad) || 0), 0);
  const kgTotal = donaciones.filter((d) => d.tipo !== "Donación Monetaria").reduce((acc, d) => acc + (parseFloat(d.cantidad) || 0), 0);
  const maxItemsUnaDonacion = Math.max(...donaciones.map((d) => (d.items?.length) || (d.cantidad > 0 ? 1 : 0)), 0);

  const stats = { total_donaciones: donaciones.length, centros_distintos: centrosUnicos, total_kg: kgTotal, max_items_una_donacion: maxItemsUnaDonacion };
  const logrosIds = new Set(logros.map((l) => l.logro.id));

  return (
    <div className="perfil">
      <div className="content-surface">
        <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
          <div>
            <h1 className="fw-bold mb-1">Mi Perfil</h1>
            <p className="m-0 c-muted">Informaci&oacute;n de tu cuenta y tu actividad.</p>
          </div>
          <Link to="/impacto" className="btn btn-accent btn-sm">
            <i className="bi bi-graph-up-arrow me-1"></i>Ver mi impacto
          </Link>
        </div>

        {guardado && (
          <div className="alert alert-success d-flex align-items-center gap-2 small py-2">
            <i className="bi bi-check-circle-fill"></i>Datos actualizados correctamente
          </div>
        )}

        <div className="row g-4">
          {/* Columna izquierda */}
          <div className="col-12 col-lg-5 d-flex flex-column gap-4">
            <div className="p-4 rounded-4 card-surface">
              <div className="d-flex align-items-center gap-3 mb-3">
                <div className="d-inline-flex align-items-center justify-content-center rounded-circle bg-accent text-white perfil-avatar">
                  <i className="bi bi-person-fill"></i>
                </div>
                <div>
                  <h2 className="fw-bold fs-5 mb-0">{user.nombre || "Usuario"}</h2>
                  <span className={`badge ${user.rol === "admin" ? "bg-warning text-dark" : "bg-primary"}`}>
                    {user.rol === "admin" ? "Administrador" : "Usuario"}
                  </span>
                </div>
              </div>

              {!editando ? (
                <div>
                  <div className="mb-2"><span className="c-muted small">RUT:</span><br />{user.rut ? `${user.rut.slice(0, -1)}-${user.rut.slice(-1)}` : ""}</div>
                  <div className="mb-2"><span className="c-muted small">Correo:</span><br />{user.email || "—"}</div>
                  <button className="btn btn-outline-accent w-100 mt-2" onClick={() => setEditando(true)}>
                    <i className="bi bi-pencil me-1"></i>Editar perfil
                  </button>
                </div>
              ) : (
                <form onSubmit={handleSave}>
                  <div className="mb-2">
                    <label className="form-label small fw-semibold">Nombre</label>
                    <input name="nombre" className={`form-control form-control-sm${formErrors.nombre ? " is-invalid" : ""}`} value={form.nombre} onChange={handleChange} />
                    {formErrors.nombre && <div className="invalid-feedback d-block">{formErrors.nombre}</div>}
                  </div>
                  <div className="mb-2">
                    <label className="form-label small fw-semibold">Correo electrónico</label>
                    <input name="email" type="email" className={`form-control form-control-sm${formErrors.email ? " is-invalid" : ""}`} value={form.email} onChange={handleChange} />
                    {formErrors.email && <div className="invalid-feedback d-block">{formErrors.email}</div>}
                  </div>
                  <div className="d-flex gap-2">
                    <button type="submit" className="btn btn-accent btn-sm flex-grow-1"><i className="bi bi-check-lg me-1"></i>Guardar</button>
                    <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setEditando(false)}>Cancelar</button>
                  </div>
                </form>
              )}
            </div>

            {/* Logros */}
            <div className="p-4 rounded-4 card-surface">
              <div className="d-flex align-items-center justify-content-between mb-3">
                <h2 className="fw-bold fs-5 mb-0">
                  <i className="bi bi-trophy-fill me-2 c-warning"></i>Mis logros
                </h2>
                <button className="btn btn-outline-accent btn-sm" onClick={() => setShowLogrosModal(true)}>
                  <i className="bi bi-grid-3x3-gap-fill me-1"></i>Ver todos
                </button>
              </div>
              {logros.length === 0 ? (
                <p className="c-muted small mb-0">A&uacute;n no has obtenido logros. &iexcl;Sigue donando!</p>
              ) : (
                <div className="d-flex flex-wrap gap-2">
                  {logros.map((l) => (
                    <div key={l.id} className="d-flex align-items-center gap-2 p-2 rounded-3 bg-page" title={l.logro.descripcion}>
                      <i className={`${l.logro.icono} fs-5 c-warning`}></i>
                      <div>
                        <div className="small fw-semibold">{l.logro.nombre}</div>
                        <div className="smaller c-muted">{new Date(l.fecha_obtenido).toLocaleDateString("es-CL")}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {showLogrosModal && (
              <LogrosModal
                todosLogros={todosLogros}
                logrosIds={logrosIds}
                stats={stats}
                onClose={() => setShowLogrosModal(false)}
              />
            )}

            {/* Agradecimientos */}
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-heart-fill me-2 c-danger"></i>Agradecimientos recibidos
              </h2>
              {agradecimientos.length === 0 ? (
                <p className="c-muted small mb-0">A&uacute;n no tienes agradecimientos.</p>
              ) : (
                <div className="d-flex flex-column gap-2" style={{ maxHeight: 300, overflowY: "auto" }}>
                  {agradecimientos.map((a) => (
                    <div key={a.id} className="p-3 rounded-3 bg-page">
                      <div className="small fw-semibold c-heading">{a.centro_nombre || `Centro #${a.centro_id}`}</div>
                      <div className="small c-muted mt-1">{a.mensaje}</div>
                      <div className="smaller c-muted mt-1">{new Date(a.fecha).toLocaleDateString("es-CL")}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Centros seguidos */}
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-heart-pulse-fill me-2 c-primary"></i>Centros que sigo
              </h2>
              {seguidos.length === 0 ? (
                <p className="c-muted small mb-0">No sigues ning&uacute;n centro. Explora centros y haz clic en el coraz&oacute;n para seguirlos.</p>
              ) : (
                <div className="d-flex flex-column gap-2">
                  {seguidos.map((s) => (
                    <div key={s.centro_id} className="d-flex align-items-center gap-2 p-2 rounded-3 bg-page">
                      <i className="bi bi-building fs-5 c-primary"></i>
                      <div>
                        <div className="small fw-semibold">{s.centro_nombre || `Centro #${s.centro_id}`}</div>
                        <div className="smaller c-muted">Siguiendo desde {new Date(s.fecha_inicio).toLocaleDateString("es-CL")}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Columna derecha */}
          <div className="col-12 col-lg-7 d-flex flex-column gap-4">
            {/* Mini resumen de impacto */}
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-graph-up-arrow me-2 c-primary"></i>Resumen de impacto
              </h2>
              <div className="row g-3">
                <div className="col-6">
                  <div className="p-3 rounded-3 bg-page text-center">
                    <div className="fw-bold fs-4 c-primary">{donaciones.length}</div>
                    <div className="small c-muted">Donaciones</div>
                  </div>
                </div>
                <div className="col-6">
                  <div className="p-3 rounded-3 bg-page text-center">
                    <div className="fw-bold fs-4 c-accent">{centrosUnicos}</div>
                    <div className="small c-muted">Centros ayudados</div>
                  </div>
                </div>
                <div className="col-6">
                  <div className="p-3 rounded-3 bg-page text-center">
                    <div className="fw-bold fs-4 c-info">{kgTotal.toFixed(0)}</div>
                    <div className="small c-muted">Kg donados</div>
                  </div>
                </div>
                <div className="col-6">
                  <div className="p-3 rounded-3 bg-page text-center">
                    <div className="fw-bold fs-4 c-danger">${monetarioTotal.toLocaleString()}</div>
                    <div className="small c-muted">Donado en dinero</div>
                  </div>
                </div>
              </div>
              <Link to="/impacto" className="btn btn-outline-accent btn-sm w-100 mt-3">
                <i className="bi bi-bar-chart-fill me-1"></i>Ver dashboard completo
              </Link>
            </div>

            {/* Donaciones recientes */}
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-clock-history me-2 c-primary"></i>Donaciones recientes
              </h2>
              {donaciones.length === 0 ? (
                <p className="c-muted small mb-0">A&uacute;n no has realizado donaciones.</p>
              ) : (
                <div className="table-responsive">
                  <table className="table table-sm table-hover mb-0">
                    <thead>
                      <tr>
                        <th>Fecha</th>
                        <th>Tipo</th>
                        <th>Cantidad</th>
                        <th>Centro</th>
                        <th>Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {donaciones.slice(0, 10).map((d) => (
                        <tr key={d.id}>
                          <td className="small c-muted">{d.fecha}</td>
                          <td className="small">{d.tipo}</td>
                          <td className="small">{d.cantidad} {d.unidad}</td>
                          <td className="small">{d.centro || d.centroId}</td>
                          <td>{estadoBadge(d.estado)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>

            {/* Certificado anual */}
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-file-earmark-pdf-fill me-2 c-danger"></i>Certificado anual
              </h2>
              <p className="small c-muted mb-3">Descarga un certificado con el resumen de tus donaciones del a&ntilde;o.</p>
              <div className="d-flex gap-2 flex-wrap">
                {[2026, 2025, 2024].filter((y) => donaciones.some((d) => d.fecha?.startsWith(String(y)))).map((year) => (
                  <button key={year} className="btn btn-outline-danger btn-sm"
                    onClick={async () => {
                      try {
                        const blob = await api.get(`/auth/certificado/${year}`, { responseType: "blob" });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        a.download = `certificado_${user.rut}_${year}.pdf`;
                        a.click();
                        URL.revokeObjectURL(url);
                      } catch { alert("Error al descargar el certificado"); }
                    }}>
                    <i className="bi bi-download me-1"></i>{year}
                  </button>
                ))}
                {![2026, 2025, 2024].some((y) => donaciones.some((d) => d.fecha?.startsWith(String(y)))) && (
                  <p className="small c-muted mb-0">A&uacute;n no hay donaciones registradas en a&ntilde;os certificables.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
