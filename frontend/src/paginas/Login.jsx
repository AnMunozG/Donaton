import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login as apiLogin } from "../api.js";
import { useAuth } from "../componentes/AuthContext";
import { validarRut, validarRequerido, validarPassword, validarForm, formatearRut, limpiarRut } from "../componentes/Validaciones.js";
import loginImg from "../assets/Login.png";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [rut, setRut] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const errores = validarForm({ origen: rut, password }, [
      { campo: "origen", nombre: "RUT", validaciones: [validarRequerido, validarRut] },
      { campo: "password", nombre: "Contraseña", validaciones: [validarRequerido, validarPassword] },
    ]);
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;
    setLoading(true);
    try {
      const user = await apiLogin(rut, password);
      login(user.rut, user.nombre, user.rol, user.email, user.token);
      navigate(user.rol === "admin" ? "/dashboard" : "/perfil");
    } catch (err) {
      setError("RUT o contraseña incorrectos");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-container">
        {/* HEADER — above both columns, offset to align with form */}
        <div className="row g-0 mb-3">
          <div className="col-md-5 d-none d-md-block"></div>
          <div className="col-md-7">
            <div className="text-center">
              <h1 className="fw-bold mb-1 c-heading">Iniciar sesión</h1>
              <p className="c-muted">Accede a tu cuenta para gestionar tus donaciones.</p>
            </div>
          </div>
        </div>

        {/* IMAGEN + CARD — same height row */}
        <div className="row g-0">
          <div className="col-md-5 d-none d-md-flex">
            <div className="img-placeholder rounded-4 login-img" style={{ backgroundImage: `url(${loginImg})` }}></div>
          </div>

          <div className="col-md-7">
            <div className="auth-form-card">
              {error && (
                <div className="alert alert-danger d-flex align-items-center gap-2 small py-2">
                  <i className="bi bi-exclamation-circle-fill"></i>{error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label fw-semibold small">RUT (sin puntos ni guión)</label>
                    <div className="input-group">
                      <span className="input-group-text"><i className="bi bi-person-fill"></i></span>
                      <input type="text" className={`form-control${formErrors.origen ? " is-invalid" : ""}`} placeholder="12.345.678-K" value={formatearRut(rut)} onChange={(e) => { const raw = limpiarRut(e.target.value); setRut(raw); if (formErrors.origen) setFormErrors({ ...formErrors, origen: "" }); }} />
                    </div>
                    {formErrors.origen && <div className="invalid-feedback d-block">{formErrors.origen}</div>}
                  </div>

                  <div className="mb-4">
                    <label className="form-label fw-semibold small">Contraseña</label>
                    <div className="input-group">
                      <span className="input-group-text"><i className="bi bi-lock-fill"></i></span>
                      <input type="password" className={`form-control${formErrors.password ? " is-invalid" : ""}`} placeholder="Ingresa tu contraseña" value={password} onChange={(e) => { setPassword(e.target.value); if (formErrors.password) setFormErrors({ ...formErrors, password: "" }); }} />
                    </div>
                    {formErrors.password && <div className="invalid-feedback d-block">{formErrors.password}</div>}
                  </div>

                <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                  <i className="bi bi-box-arrow-in-right me-2"></i>{loading ? "Validando..." : "Iniciar sesión"}
                </button>
              </form>

              <div className="text-center mt-3">
                <small className="c-muted">
                  ¿No tienes cuenta? <a href="/registro" className="auth-link">Regístrate aquí</a>
                </small>
              </div>
              <div className="auth-divider text-center">
                <small className="c-muted">
                  <strong className="c-heading">Prueba:</strong> Admin: 11111111-1 / admin1234
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
