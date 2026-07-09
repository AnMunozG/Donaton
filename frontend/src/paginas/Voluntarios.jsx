import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../componentes/AuthContext";
import {
  getMiPerfilVoluntario, crearVoluntario, actualizarVoluntario,
  getVoluntarios, getHabilidadesVoluntario,
  getNecesidades,
} from "../api.js";

const DISPONIBILIDAD_OPTS = [
  { value: "diaria", label: "Diaria" },
  { value: "semanal", label: "Semanal" },
  { value: "fines_semana", label: "Fines de semana" },
  { value: "emergencia", label: "Solo emergencias" },
];

export default function Voluntarios() {
  const { isAuth, user } = useAuth();
  const navigate = useNavigate();

  const [perfil, setPerfil] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [habilidades, setHabilidades] = useState([]);
  const [oportunidades, setOportunidades] = useState([]);

  const [form, setForm] = useState({
    disponibilidad: "emergencia",
    habilidades: [],
    centro_preferido: "",
  });
  const [formError, setFormError] = useState("");
  const [guardando, setGuardando] = useState(false);
  const [exito, setExito] = useState("");

  useEffect(() => {
    getHabilidadesVoluntario().then(setHabilidades);
    getNecesidades().then((todas) => {
      const voluntariado = (Array.isArray(todas) ? todas : [])
        .filter((n) => n.recurso === "Voluntariado / Mano de Obra" && n.estado === "Activa");
      setOportunidades(voluntariado);
    });
  }, []);

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
          centro_preferido: p.centro_preferido || "",
        });
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
    setGuardando(true);
    try {
      if (perfil) {
        await actualizarVoluntario(perfil.id, form);
        setExito("Perfil de voluntario actualizado correctamente.");
      } else {
        await crearVoluntario(form);
        setExito("Solicitud enviada. Un administrador revisará tu inscripción y te activará pronto.");
      }
      const actualizado = await getMiPerfilVoluntario();
      setPerfil(actualizado);
    } catch (err) {
      setFormError(err?.response?.data?.error || "Error al guardar el perfil de voluntario.");
    } finally {
      setGuardando(false);
    }
  };

  if (cargando) {
    return <div className="container mt-5 text-center"><div className="spinner-border" /></div>;
  }

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-lg-8 mx-auto">
          <h1 className="mb-4">
            <i className="bi bi-person-arms-up me-2"></i>Voluntarios
          </h1>

          {exito && (
            <div className="alert alert-success alert-dismissible fade show">
              {exito}
              <button type="button" className="btn-close" onClick={() => setExito("")} />
            </div>
          )}

          {!isAuth ? (
            <div className="card shadow-sm mb-4">
              <div className="card-body text-center p-5">
                <i className="bi bi-person-circle" style={{ fontSize: "4rem", color: "#DD4444" }}></i>
                <h3 className="mt-3">Inicia sesión para ser voluntario</h3>
                <p className="text-muted">Debes tener una cuenta registrada para inscribirte como voluntario.</p>
                <button className="btn btn-accent btn-lg me-2" onClick={() => navigate("/login")}>
                  Iniciar sesión
                </button>
                <button className="btn btn-outline-accent btn-lg" onClick={() => navigate("/registro")}>
                  Crear cuenta
                </button>
              </div>
            </div>
          ) : (
            <div className="card shadow-sm mb-4">
              <div className="card-header">
                <h5 className="mb-0">
                  <i className="bi bi-person-fill me-2"></i>
                  {perfil ? "Mi perfil de voluntario" : "Regístrate como voluntario"}
                </h5>
              </div>
              <div className="card-body">
                <div className="mb-3">
                  <strong>RUT:</strong> {user?.rut}
                </div>
                {perfil && (
                  <div className="mb-3">
                    <strong>Estado:</strong>{" "}
                    <span className={`badge ${perfil.estado === "activo" ? "bg-success" : perfil.estado === "pendiente" ? "bg-warning text-dark" : "bg-secondary"}`}>
                      {perfil.estado === "activo" ? "Activo" : perfil.estado === "pendiente" ? "Pendiente de aprobación" : "Inactivo"}
                    </span>
                    {perfil.estado === "pendiente" && (
                      <small className="text-muted ms-2">Tu solicitud está siendo revisada por un administrador.</small>
                    )}
                  </div>
                )}

                {formError && <div className="alert alert-danger py-2">{formError}</div>}

                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label">Disponibilidad</label>
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
                    <label className="form-label">Habilidades</label>
                    <div className="row g-2">
                      {habilidades.map((h) => (
                        <div key={h.code} className="col-md-4 col-sm-6">
                          <div
                            className={`form-check volunteer-skill-card p-2 rounded border cursor-pointer ${
                              form.habilidades.includes(h.code) ? "border-accent bg-accent-light" : ""
                            }`}
                            onClick={() => toggleHabilidad(h.code)}
                          >
                            <input
                              type="checkbox"
                              className="form-check-input"
                              checked={form.habilidades.includes(h.code)}
                              onChange={() => toggleHabilidad(h.code)}
                            />
                            <label className="form-check-label ms-2">
                              <strong>{h.nombre}</strong>
                              <small className="d-block text-muted">{h.descripcion}</small>
                            </label>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Centro de acopio preferido (opcional)</label>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="ID del centro o déjalo vacío"
                      value={form.centro_preferido}
                      onChange={(e) => setForm({ ...form, centro_preferido: e.target.value })}
                    />
                    <div className="form-text">Selecciona un centro si tienes preferencia por alguno.</div>
                  </div>

                  <button type="submit" className="btn btn-accent" disabled={guardando}>
                    {guardando ? (
                      <><span className="spinner-border spinner-border-sm me-1" /> Guardando...</>
                    ) : (
                      <><i className="bi bi-check-lg me-1"></i>{perfil ? "Actualizar perfil" : "Registrarme como voluntario"}</>
                    )}
                  </button>
                </form>
              </div>
            </div>
          )}

          {perfil && (
            <div className="card shadow-sm mb-4">
              <div className="card-header">
                <h5 className="mb-0"><i className="bi bi-clock-history me-2"></i>Horas registradas</h5>
              </div>
              <div className="card-body text-center">
                <span className="display-4 fw-bold" style={{ color: "#DD4444" }}>
                  {perfil.horas_acumuladas || 0}
                </span>
                <span className="h4 ms-2 text-muted">horas</span>
                <p className="text-muted mt-2">Total de horas como voluntario</p>
              </div>
            </div>
          )}

          <div className="card shadow-sm">
            <div className="card-header">
              <h5 className="mb-0"><i className="bi bi-megaphone-fill me-2"></i>Oportunidades de voluntariado</h5>
            </div>
            <div className="card-body">
              {oportunidades.length === 0 ? (
                <p className="text-muted mb-0">No hay oportunidades de voluntariado disponibles en este momento.</p>
              ) : (
                <div className="list-group">
                  {oportunidades.map((op) => (
                    <div key={op.id} className="list-group-item list-group-item-action">
                      <div className="d-flex w-100 justify-content-between">
                        <h6 className="mb-1">{op.recurso}</h6>
                        <span className={`badge ${op.urgencia === "Alta" ? "bg-danger" : op.urgencia === "Media" ? "bg-warning" : "bg-secondary"}`}>
                          {op.urgencia}
                        </span>
                      </div>
                      <p className="mb-1 text-muted small">{op.descripcion}</p>
                      <small><i className="bi bi-geo-alt me-1"></i>{op.centro}</small>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
