import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { validarRut, validarRequerido, validarEmail, validarPassword, validarConfirmacion, validarForm, formatearRut, limpiarRut } from "../componentes/Validaciones.js";
import { crearCuenta } from "../api.js";

export default function Registro() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ rut: "", nombre: "", email: "", password: "", confirmacion: "", terms: false });
  const [enviado, setEnviado] = useState(false);
  const [error, setError] = useState("");
  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const value = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    setForm({ ...form, [e.target.name]: value });
    if (formErrors[e.target.name]) setFormErrors({ ...formErrors, [e.target.name]: "" });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const errores = validarForm(form, [
      { campo: "rut", nombre: "RUT", validaciones: [validarRequerido, validarRut] },
      { campo: "nombre", nombre: "Nombre completo", validaciones: [validarRequerido] },
      { campo: "email", nombre: "Correo electrónico", validaciones: [validarRequerido, validarEmail] },
      { campo: "password", nombre: "Contraseña", validaciones: [validarRequerido, validarPassword] },
    ]);
    const confMsg = validarConfirmacion(form.password, form.confirmacion);
    if (confMsg) errores.confirmacion = confMsg;
    if (!form.terms) errores.terms = "Debes aceptar los términos y condiciones";
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;
    try {
      await crearCuenta(form.rut, { nombre: form.nombre, email: form.email, password: form.password });
      setEnviado(true);
      setForm({ rut: "", nombre: "", email: "", password: "", confirmacion: "", terms: false });
      setTimeout(() => navigate("/login"), 2000);
    } catch {
      setError("Ese RUT ya está registrado");
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-container auth-container-wide">
        {/* HEADER — above both columns, offset to align with form */}
        <div className="row g-0 mb-3">
          <div className="col-md-5 d-none d-md-block"></div>
          <div className="col-md-7">
            <div className="text-center">
              <h1 className="fw-bold mb-1 c-heading">Registro de Socios</h1>
              <p className="c-muted">Únete a nuestra comunidad de donantes y haz la diferencia.</p>
            </div>
          </div>
        </div>

        {/* IMAGEN + CARD — same height row */}
        <div className="row g-0">
          <div className="col-md-5 d-none d-md-flex">
            <div className="img-placeholder rounded-4 login-img" style={{ backgroundImage: "url(https://www.chile.gob.cl/yakarta/site/artic/20241007/imag/foto_0000000220241007120604/Fiestas_Patrias.jpeg)" }}></div>
          </div>

          <div className="col-md-7">
            <div className="auth-form-card auth-form-card-wide">
              {error && (
                <div className="alert alert-danger d-flex align-items-center gap-2 small py-2">
                  <i className="bi bi-exclamation-circle-fill"></i>{error}
                </div>
              )}
              {enviado && (
                <div className="alert alert-success d-flex align-items-center gap-2 small py-2">
                  <i className="bi bi-check-circle-fill"></i>¡Registro exitoso! Redirigiendo al inicio de sesión...
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="row g-3">
                  <div className="col-12">
                    <label className="form-label fw-semibold small">RUT (sin puntos ni guión)</label>
                    <div className="input-group">
                      <span className="input-group-text"><i className="bi bi-person-fill"></i></span>
                      <input type="text" name="rut" className={`form-control${formErrors.rut ? " is-invalid" : ""}`} placeholder="12.345.678-K" value={formatearRut(form.rut)} onChange={(e) => { const raw = limpiarRut(e.target.value); setForm({ ...form, rut: raw }); if (formErrors.rut) setFormErrors({ ...formErrors, rut: "" }); }} />
                    </div>
                    {formErrors.rut && <div className="invalid-feedback d-block">{formErrors.rut}</div>}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold small">Nombre completo</label>
                    <div className="input-group">
                      <span className="input-group-text"><i className="bi bi-person-fill"></i></span>
                      <input type="text" name="nombre" className={`form-control${formErrors.nombre ? " is-invalid" : ""}`} placeholder="Juan Pérez" value={form.nombre} onChange={handleChange} />
                    </div>
                    {formErrors.nombre && <div className="invalid-feedback d-block">{formErrors.nombre}</div>}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold small">Correo electrónico</label>
                    <div className="input-group">
                      <span className="input-group-text"><i className="bi bi-envelope-fill"></i></span>
                      <input type="email" name="email" className={`form-control${formErrors.email ? " is-invalid" : ""}`} placeholder="correo@ejemplo.cl" value={form.email} onChange={handleChange} />
                    </div>
                    {formErrors.email && <div className="invalid-feedback d-block">{formErrors.email}</div>}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold small">Contraseña</label>
                    <div className="input-group">
                      <span className="input-group-text"><i className="bi bi-lock-fill"></i></span>
                      <input type="password" name="password" className={`form-control${formErrors.password ? " is-invalid" : ""}`} placeholder="Mínimo 8 caracteres" value={form.password} onChange={handleChange} />
                    </div>
                    {formErrors.password && <div className="invalid-feedback d-block">{formErrors.password}</div>}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold small">Confirmar contraseña</label>
                    <div className="input-group">
                      <span className="input-group-text"><i className="bi bi-lock-fill"></i></span>
                      <input type="password" name="confirmacion" className={`form-control${formErrors.confirmacion ? " is-invalid" : ""}`} placeholder="Repite la contraseña" value={form.confirmacion} onChange={handleChange} />
                    </div>
                    {formErrors.confirmacion && <div className="invalid-feedback d-block">{formErrors.confirmacion}</div>}
                  </div>

                  <div className="col-12">
                    <div className="form-check">
                      <input type="checkbox" name="terms" className={`form-check-input${formErrors.terms ? " is-invalid" : ""}`} id="terms" checked={form.terms} onChange={handleChange} />
                      <label className="form-check-label small c-muted" htmlFor="terms">
                        Acepto los <a href="#" className="auth-link">términos y condiciones</a>.
                      </label>
                      {formErrors.terms && <div className="invalid-feedback d-block">{formErrors.terms}</div>}
                    </div>
                  </div>
                </div>

                <button type="submit" className="btn btn-primary w-100 mt-3">
                  <i className="bi bi-person-plus-fill me-2"></i>Registrarse
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
