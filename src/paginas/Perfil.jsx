import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../componentes/AuthContext";
import { getDonaciones, actualizarCuenta } from "../api.js";
import { validarRequerido, validarEmail, validarPassword, validarConfirmacion, validarForm } from "../componentes/Validaciones.js";

export default function Perfil() {
  const { user, isAuth, updateUser } = useAuth();
  const [donaciones, setDonaciones] = useState([]);
  const [editando, setEditando] = useState(false);
  const [guardado, setGuardado] = useState(false);
  const [form, setForm] = useState({ nombre: "", email: "", password: "", confirmacion: "" });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    if (!isAuth) return;
    getDonaciones().then((lista) => {
      setDonaciones(lista.filter((d) => d.origen === user.rut).reverse());
    });
  }, [isAuth, user.rut]);

  useEffect(() => {
    if (editando) setForm({ nombre: user.nombre || "", email: user.email || "", password: "", confirmacion: "" });
  }, [editando, user.nombre, user.email]);

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
    if (form.password) {
      reglas.push(
        { campo: "password", nombre: "Contraseña", validaciones: [validarRequerido, validarPassword] },
      );
    }
    const errores = validarForm(form, reglas);
    if (form.password) {
      const confMsg = validarConfirmacion(form.password, form.confirmacion);
      if (confMsg) errores.confirmacion = confMsg;
    }
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;
    const data = { nombre: form.nombre, email: form.email };
    if (form.password) data.password = form.password;
    try {
      await actualizarCuenta(user.rut, data);
      updateUser(data);
      setGuardado(true);
      setEditando(false);
      setTimeout(() => setGuardado(false), 3000);
    } catch {
      setFormErrors({ general: "Error al guardar" });
    }
  };

  const estadoBadge = (est) => {
    const map = { "Entregado": "bg-success", "En tránsito": "bg-info text-dark", "En acopio": "bg-warning text-dark" };
    return <span className={`badge ${map[est] || "bg-secondary"}`}>{est}</span>;
  };

  return (
    <div className="perfil">
      <div className="content-surface">
        <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
          <div>
            <h1 className="fw-bold mb-1">Mi Perfil</h1>
            <p className="m-0 c-muted">Información de tu cuenta y donaciones recientes.</p>
          </div>
        </div>

        {guardado && (
          <div className="alert alert-success d-flex align-items-center gap-2 small py-2">
            <i className="bi bi-check-circle-fill"></i>Datos actualizados correctamente
          </div>
        )}

        <div className="row g-4">
          {/* Columna izquierda: datos personales */}
          <div className="col-12 col-lg-5">
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
                  <div className="mb-2">
                    <label className="form-label small fw-semibold">Nueva contraseña <span className="c-muted">(opcional)</span></label>
                    <input name="password" type="password" className={`form-control form-control-sm${formErrors.password ? " is-invalid" : ""}`} placeholder="Mínimo 8 caracteres" value={form.password} onChange={handleChange} />
                    {formErrors.password && <div className="invalid-feedback d-block">{formErrors.password}</div>}
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold">Confirmar contraseña</label>
                    <input name="confirmacion" type="password" className={`form-control form-control-sm${formErrors.confirmacion ? " is-invalid" : ""}`} placeholder="Repite la contraseña" value={form.confirmacion} onChange={handleChange} />
                    {formErrors.confirmacion && <div className="invalid-feedback d-block">{formErrors.confirmacion}</div>}
                  </div>
                  <div className="d-flex gap-2">
                    <button type="submit" className="btn btn-accent btn-sm flex-grow-1"><i className="bi bi-check-lg me-1"></i>Guardar</button>
                    <button type="button" className="btn btn-outline-secondary btn-sm" onClick={() => setEditando(false)}>Cancelar</button>
                  </div>
                </form>
              )}
            </div>
          </div>

          {/* Columna derecha: donaciones recientes */}
          <div className="col-12 col-lg-7">
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3">
                <i className="bi bi-clock-history me-2 c-primary"></i>Donaciones recientes
              </h2>
              {donaciones.length === 0 ? (
                <p className="c-muted small mb-0">Aún no has realizado donaciones.</p>
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
          </div>
        </div>
      </div>
    </div>
  );
}
