import { useState, useEffect, useRef } from "react";
import { getTiposRecurso, getUnidadesPorTipo, getCamposPorTipo, getCentros, agregarNecesidadUsuario } from "../api.js";
import RichTextEditor from "../componentes/RichTextEditor";
import { validarRequerido, validarEnteroPositivo, validarRut, validarForm, formatearRut, limpiarRut } from "../componentes/Validaciones.js";

const DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];

const URGENCIA_STYLES = {
  "": { label: "Pendiente", class: "bg-secondary", icon: "bi-clock" },
  "BAJA": { label: "Baja", class: "bg-success", icon: "bi-arrow-down-circle" },
  "MEDIA": { label: "Media", class: "bg-warning text-dark", icon: "bi-dash-circle" },
  "ALTA": { label: "Alta", class: "bg-danger", icon: "bi-exclamation-circle" },
};

const INIT_FORM = {
  reportadoPor: "", contactoEmail: "", contactoTel: "",
  recurso: "", cantidad: "", unidad: "", recursoPersonalizado: "",
  descripcion: "", centroAcopio: "", fechaLimite: "",
  actividad: "", horaDesde: "", horaHasta: "", ubicacion: "", dias: [], numVoluntarios: "", habilidades: "", tipoVoluntariado: "",
};

export default function Necesidades() {
  const [tipoNecesidad, setTipoNecesidad] = useState(""); // "" | "recurso" | "voluntarios"
  const [tiposRecurso, setTiposRecurso] = useState([]);
  const [unidadesPorTipo, setUnidadesPorTipo] = useState({});
  const [camposPorTipo, setCamposPorTipo] = useState({});
  const [centros, setCentros] = useState([]);

  const [form, setForm] = useState({ ...INIT_FORM });
  const [enviado, setEnviado] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const enviadoTimer = useRef(null);

  useEffect(() => {
    return () => clearTimeout(enviadoTimer.current);
  }, []);

  useEffect(() => {
    Promise.all([
      getTiposRecurso(),
      getUnidadesPorTipo(),
      getCamposPorTipo(),
      getCentros(),
    ]).then(([tipos, uMap, campos, centrosData]) => {
      setTiposRecurso(tipos);
      setUnidadesPorTipo(uMap);
      setCamposPorTipo(campos);
      setCentros(centrosData);
    });
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    if (type === "checkbox") {
      setForm((prev) => ({
        ...prev,
        dias: checked ? [...prev.dias, value] : prev.dias.filter((d) => d !== value),
      }));
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
    if (formErrors[name]) setFormErrors((prev) => ({ ...prev, [name]: "" }));
  };

  const handleRecursoChange = (e) => {
    const nuevoRecurso = e.target.value;
    const unidades = unidadesPorTipo[nuevoRecurso] || [];
    setForm((prev) => ({ ...prev, recurso: nuevoRecurso, unidad: unidades[0] || "", recursoPersonalizado: "" }));
  };

  const handleDetalleChange = (key, value) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const seleccionarTipo = (tipo) => {
    setTipoNecesidad(tipo);
    setForm({ ...INIT_FORM });
    setFormErrors({});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const reglas = [
      { campo: "reportadoPor", nombre: "RUT reportante", validaciones: [validarRequerido, validarRut] },
    ];

    if (tipoNecesidad === "recurso") {
      reglas.push(
        { campo: "recurso", nombre: "Recurso", validaciones: [validarRequerido] },
        { campo: "cantidad", nombre: "Cantidad", validaciones: [validarRequerido, validarEnteroPositivo] },
        { campo: "unidad", nombre: "Unidad", validaciones: [validarRequerido] },
        { campo: "centroAcopio", nombre: "Centro de acopio", validaciones: [validarRequerido] },
      );
    } else if (tipoNecesidad === "voluntarios") {
      reglas.push(
        { campo: "actividad", nombre: "Actividad", validaciones: [validarRequerido] },
        { campo: "horaDesde", nombre: "Horario desde", validaciones: [validarRequerido] },
        { campo: "horaHasta", nombre: "Horario hasta", validaciones: [validarRequerido] },
        { campo: "ubicacion", nombre: "Ubicación", validaciones: [validarRequerido] },
        { campo: "numVoluntarios", nombre: "N° de voluntarios", validaciones: [validarRequerido, validarEnteroPositivo] },
        { campo: "centroAcopio", nombre: "Centro de acopio", validaciones: [validarRequerido] },
      );
    }

    const errores = validarForm(form, reglas);
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;

    try {
      const detalles = {};
      if (form.contactoEmail) detalles.contactoEmail = form.contactoEmail;
      if (form.contactoTel) detalles.contactoTel = form.contactoTel;
      if (form.fechaLimite) detalles.fechaLimite = form.fechaLimite;

      if (tipoNecesidad === "recurso") {
        const recursoFinal = form.recurso === "Otros" && form.recursoPersonalizado
          ? `Otros - ${form.recursoPersonalizado}`
          : form.recurso;
        camposAdicionales.forEach((campo) => {
          if (form[campo.name]) detalles[campo.name] = form[campo.name];
        });
        detalles.tipoNecesidad = "recurso";

        await agregarNecesidadUsuario({
          recurso: recursoFinal,
          cantidad: form.cantidad,
          unidad: form.unidad,
          descripcion: form.descripcion,
          reportadoPor: form.reportadoPor,
          centroId: form.centroAcopio,
          urgencia: "Pendiente",
          detalles,
        });
      } else {
        detalles.tipoNecesidad = "voluntarios";
        detalles.actividad = form.actividad;
        detalles.horaDesde = form.horaDesde;
        detalles.horaHasta = form.horaHasta;
        detalles.ubicacion = form.ubicacion;
        detalles.dias = form.dias;
        detalles.numVoluntarios = parseInt(form.numVoluntarios);
        detalles.habilidades = form.habilidades;
        detalles.tipoVoluntariado = form.tipoVoluntariado;

        await agregarNecesidadUsuario({
          recurso: "Voluntariado",
          cantidad: form.numVoluntarios,
          unidad: "voluntarios",
          descripcion: form.descripcion,
          reportadoPor: form.reportadoPor,
          centroId: form.centroAcopio,
          urgencia: "Pendiente",
          detalles,
        });
      }

      setEnviado(true);
      setFormErrors({});
      clearTimeout(enviadoTimer.current);
      enviadoTimer.current = setTimeout(() => setEnviado(false), 4000);
      setForm({ ...INIT_FORM });
    } catch {
      alert("Error al reportar la necesidad. Intente nuevamente.");
    }
  };

  const unidadesDisponibles = unidadesPorTipo[form.recurso] || [];
  const camposAdicionales = camposPorTipo[form.recurso] || [];
  const urgenciaStyle = URGENCIA_STYLES[""];

  return (
    <div className="necesidades">
      <div className="content-surface">
        <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
          <div>
            <h1 className="fw-bold mb-1">Necesidades en Terreno</h1>
            <p className="m-0 c-muted">Reporta necesidades urgentes para coordinar la ayuda de forma eficiente.</p>
          </div>
          <span className="page-header-pill warning-pill">
            <i className="bi bi-exclamation-triangle-fill"></i> Reporte directo
          </span>
        </div>

        <div className="row g-4">
          <div className="col-12 col-lg-5">
            <div className="img-placeholder rounded-4" style={{ backgroundImage: "url(https://chile.iom.int/sites/g/files/tmzbdl906/files/coim-chile-francisca-salinas_oim-entrega-alimentos_1.jpg)" }}></div>
          </div>

          <div className="col-12 col-lg-7">
            <div className="p-4 rounded-4 card-surface">
              <h2 className="fw-bold fs-5 mb-3 c-heading">
                <i className="bi bi-flag-fill me-2 c-primary"></i>Reportar necesidad
              </h2>

              {enviado && (
                <div className="alert alert-success d-flex align-items-center gap-2 small py-2">
                  <i className="bi bi-check-circle-fill"></i>Necesidad reportada correctamente
                </div>
              )}

              {!tipoNecesidad ? (
                <div className="text-center py-4">
                  <p className="c-muted mb-3">¿Qué tipo de necesidad deseas reportar?</p>
                  <div className="d-flex justify-content-center gap-3">
                    <button type="button" className="btn btn-outline-primary btn-lg px-4 py-3"
                      onClick={() => seleccionarTipo("recurso")}>
                      <i className="bi bi-box-seam d-block fs-2 mb-2"></i>
                      <span className="fw-semibold">Recurso</span>
                      <small className="d-block c-muted mt-1">Alimentos, ropa, insumos...</small>
                    </button>
                    <button type="button" className="btn btn-outline-accent btn-lg px-4 py-3"
                      onClick={() => seleccionarTipo("voluntarios")}>
                      <i className="bi bi-people-fill d-block fs-2 mb-2"></i>
                      <span className="fw-semibold">Voluntarios</span>
                      <small className="d-block c-muted mt-1">Mano de obra, apoyo en terreno...</small>
                    </button>
                  </div>
                </div>
              ) : (
                <form onSubmit={handleSubmit}>
                  <div className="d-flex align-items-center gap-2 mb-3">
                    <span className={`badge d-flex align-items-center gap-1 py-1 px-2 ${tipoNecesidad === "recurso" ? "bg-primary" : "bg-accent"}`}>
                      <i className={`bi ${tipoNecesidad === "recurso" ? "bi-box-seam" : "bi-people-fill"}`}></i>
                      {tipoNecesidad === "recurso" ? "Recurso" : "Voluntarios"}
                    </span>
                    <button type="button" className="btn btn-sm btn-outline-secondary py-0 px-2"
                      onClick={() => { setTipoNecesidad(""); setForm({ ...INIT_FORM }); setFormErrors({}); }}>
                      <i className="bi bi-arrow-left me-1"></i>Cambiar tipo
                    </button>
                  </div>

                  <div className="row g-3">
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small">RUT del reportante</label>
                      <input type="text" name="reportadoPor"
                        className={`form-control${formErrors.reportadoPor ? " is-invalid" : ""}`}
                        placeholder="12.345.678-K" value={formatearRut(form.reportadoPor)}
                        onChange={(e) => { const raw = limpiarRut(e.target.value); setForm((prev) => ({ ...prev, reportadoPor: raw })); if (formErrors.reportadoPor) setFormErrors((prev) => ({ ...prev, reportadoPor: "" })); }} />
                      {formErrors.reportadoPor && <div className="invalid-feedback d-block">{formErrors.reportadoPor}</div>}
                    </div>
                    <div className="col-md-3">
                      <label className="form-label fw-semibold small">Email contacto</label>
                      <input type="email" name="contactoEmail" className="form-control"
                        placeholder="correo@ejemplo.cl" value={form.contactoEmail} onChange={handleChange} />
                    </div>
                    <div className="col-md-3">
                      <label className="form-label fw-semibold small">Teléfono contacto</label>
                      <input type="tel" name="contactoTel" className="form-control"
                        placeholder="+56 9 1234 5678" value={form.contactoTel} onChange={handleChange} />
                    </div>
                  </div>

                  {/* ── Formulario Recurso ── */}
                  {tipoNecesidad === "recurso" && (
                    <div className="mt-3 p-3 rounded-3 bg-page b-card">
                      <h3 className="fs-6 fw-bold mb-3 c-heading">
                        <i className="bi bi-box-seam me-1 c-primary"></i>Recurso solicitado
                      </h3>
                      <div className="row g-3">
                        <div className="col-md-6">
                          <label className="form-label fw-semibold small">Recurso necesitado</label>
                          <select name="recurso" className={`form-select${formErrors.recurso ? " is-invalid" : ""}`}
                            value={form.recurso} onChange={handleRecursoChange}>
                            <option value="">Selecciona...</option>
                            {tiposRecurso.map((t) => <option key={t}>{t}</option>)}
                          </select>
                          {form.recurso === "Otros" && (
                            <input type="text" name="recursoPersonalizado" className="form-control mt-2"
                              placeholder="Describe el recurso..." value={form.recursoPersonalizado || ""} onChange={handleChange} />
                          )}
                          {formErrors.recurso && <div className="invalid-feedback d-block">{formErrors.recurso}</div>}
                        </div>

                        <div className="col-md-6">
                          <label className="form-label fw-semibold small">Cantidad requerida</label>
                          <div className="input-group">
                            <input type="number" name="cantidad" className={`form-control${formErrors.cantidad ? " is-invalid" : ""}`}
                              placeholder="Ej: 100" min="1" step="1" value={form.cantidad} onChange={handleChange} />
                            <select name="unidad" className={`form-select small-form-select-width${formErrors.unidad ? " is-invalid" : ""}`}
                              value={form.unidad} onChange={handleChange} disabled={!form.recurso}>
                              {unidadesDisponibles.map((u) => <option key={u} value={u}>{u}</option>)}
                            </select>
                          </div>
                          {formErrors.cantidad && <div className="invalid-feedback d-block">{formErrors.cantidad}</div>}
                          {formErrors.unidad && <div className="invalid-feedback d-block">{formErrors.unidad}</div>}
                        </div>
                      </div>

                      {camposAdicionales.length > 0 && (
                        <div className="mt-3 p-3 rounded-3 bg-page b-card">
                          <h4 className="fs-6 fw-bold mb-2 c-heading">
                            <i className="bi bi-info-circle-fill me-2 c-primary"></i>Detalles adicionales
                          </h4>
                          <div className="row g-2">
                            {camposAdicionales.map((campo) => (
                              <div key={campo.name} className="col-md-6">
                                <label className="form-label fw-semibold small">{campo.label}</label>
                                {campo.type === "select" ? (
                                  <select className="form-select form-select-sm"
                                    value={form[campo.name] || ""}
                                    onChange={(e) => handleDetalleChange(campo.name, e.target.value)}>
                                    <option value="">Selecciona...</option>
                                    {campo.options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
                                  </select>
                                ) : campo.type === "textarea" ? (
                                  <RichTextEditor content={form[campo.name] || ""}
                                    onChange={(value) => handleDetalleChange(campo.name, value)}
                                    placeholder={`Escribe ${campo.label.toLowerCase()}...`} />
                                ) : (
                                  <input type={campo.type === "date" ? "date" : "text"}
                                    className="form-control form-control-sm" placeholder={campo.placeholder || ""}
                                    value={form[campo.name] || ""}
                                    onChange={(e) => handleDetalleChange(campo.name, e.target.value)} />
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      <div className="mt-3">
                        <label className="form-label fw-semibold small">Centro de acopio</label>
                        <select name="centroAcopio" className={`form-select${formErrors.centroAcopio ? " is-invalid" : ""}`}
                          value={form.centroAcopio} onChange={handleChange}>
                          <option value="">Selecciona...</option>
                          {centros.map((centro) => <option key={centro.id} value={centro.id}>{centro.nombre}</option>)}
                        </select>
                        {formErrors.centroAcopio && <div className="invalid-feedback d-block">{formErrors.centroAcopio}</div>}
                      </div>

                      <div className="mt-3">
                        <label className="form-label fw-semibold small">Fecha límite</label>
                        <input type="date" name="fechaLimite" className="form-control"
                          value={form.fechaLimite} onChange={handleChange} />
                      </div>
                    </div>
                  )}

                  {/* ── Formulario Voluntarios ── */}
                  {tipoNecesidad === "voluntarios" && (
                    <div className="mt-3 p-3 rounded-3 bg-page b-card">
                      <h3 className="fs-6 fw-bold mb-3 c-heading">
                        <i className="bi bi-people-fill me-1 c-accent"></i>Convocatoria de voluntarios
                      </h3>
                      <div className="row g-3">
                        <div className="col-12">
                          <label className="form-label fw-semibold small">Actividad a realizar</label>
                          <RichTextEditor content={form.actividad}
                            onChange={(value) => handleDetalleChange("actividad", value)}
                            placeholder="Describe en qué consiste la actividad..." />
                          {formErrors.actividad && <div className="invalid-feedback d-block">{formErrors.actividad}</div>}
                        </div>

                        <div className="col-md-4">
                          <label className="form-label fw-semibold small">Horario desde</label>
                          <input type="time" name="horaDesde" className={`form-control${formErrors.horaDesde ? " is-invalid" : ""}`}
                            value={form.horaDesde} onChange={handleChange} />
                          {formErrors.horaDesde && <div className="invalid-feedback d-block">{formErrors.horaDesde}</div>}
                        </div>

                        <div className="col-md-4">
                          <label className="form-label fw-semibold small">Horario hasta</label>
                          <input type="time" name="horaHasta" className={`form-control${formErrors.horaHasta ? " is-invalid" : ""}`}
                            value={form.horaHasta} onChange={handleChange} />
                          {formErrors.horaHasta && <div className="invalid-feedback d-block">{formErrors.horaHasta}</div>}
                        </div>

                        <div className="col-md-4">
                          <label className="form-label fw-semibold small">N° de voluntarios necesarios</label>
                          <input type="number" name="numVoluntarios" className={`form-control${formErrors.numVoluntarios ? " is-invalid" : ""}`}
                            placeholder="Ej: 10" min="1" value={form.numVoluntarios} onChange={handleChange} />
                          {formErrors.numVoluntarios && <div className="invalid-feedback d-block">{formErrors.numVoluntarios}</div>}
                        </div>

                        <div className="col-12">
                          <label className="form-label fw-semibold small">Ubicación donde se trabajará</label>
                          <input type="text" name="ubicacion" className={`form-control${formErrors.ubicacion ? " is-invalid" : ""}`}
                            placeholder="Calle, comuna, punto de referencia..." value={form.ubicacion} onChange={handleChange} />
                          {formErrors.ubicacion && <div className="invalid-feedback d-block">{formErrors.ubicacion}</div>}
                        </div>

                        <div className="col-12">
                          <label className="form-label fw-semibold small">Días de la semana</label>
                          <div className="d-flex flex-wrap gap-2">
                            {DIAS_SEMANA.map((dia) => (
                              <label key={dia} className="d-flex align-items-center gap-1 form-check-label small">
                                <input type="checkbox" className="form-check-input" value={dia}
                                  checked={form.dias.includes(dia)} onChange={handleChange} />
                                {dia}
                              </label>
                            ))}
                          </div>
                        </div>

                        <div className="col-md-6">
                          <label className="form-label fw-semibold small">Tipo de voluntariado</label>
                          <select name="tipoVoluntariado" className="form-select" value={form.tipoVoluntariado} onChange={handleChange}>
                            <option value="">Selecciona...</option>
                            <option value="Terreno">Terreno (trabajo en sitio)</option>
                            <option value="Logística">Logística y bodega</option>
                            <option value="Administrativo">Administrativo / Gestión</option>
                            <option value="Profesional">Profesional (médico, legal, etc.)</option>
                            <option value="Otros">Otros</option>
                          </select>
                        </div>

                        <div className="col-md-6">
                          <label className="form-label fw-semibold small">Habilidades requeridas</label>
                          <input type="text" name="habilidades" className="form-control"
                            placeholder="Ej: Manejo de herramientas, primeros auxilios..." value={form.habilidades} onChange={handleChange} />
                        </div>

                        <div className="col-12">
                          <label className="form-label fw-semibold small">Centro de acopio de referencia</label>
                          <select name="centroAcopio" className={`form-select${formErrors.centroAcopio ? " is-invalid" : ""}`}
                            value={form.centroAcopio} onChange={handleChange}>
                            <option value="">Selecciona...</option>
                            {centros.map((centro) => <option key={centro.id} value={centro.id}>{centro.nombre}</option>)}
                          </select>
                          {formErrors.centroAcopio && <div className="invalid-feedback d-block">{formErrors.centroAcopio}</div>}
                        </div>

                        <div className="col-12">
                          <label className="form-label fw-semibold small">Fecha límite</label>
                          <input type="date" name="fechaLimite" className="form-control"
                            value={form.fechaLimite} onChange={handleChange} />
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="mt-3">
                    <label className="form-label fw-semibold small">Descripción detallada</label>
                    <RichTextEditor content={form.descripcion}
                      onChange={(value) => handleDetalleChange("descripcion", value)}
                      placeholder={tipoNecesidad === "voluntarios" ? "Describe el contexto, objetivos y cualquier información relevante para los voluntarios..." : "Describe la necesidad en detalle..."} />
                  </div>

                  <div className="mt-3 d-flex align-items-center gap-2 p-2 rounded-3 small"
                    style={{ background: "var(--bg-page)" }}>
                    <span className={`badge ${urgenciaStyle.class} d-flex align-items-center gap-1 py-1 px-2`}>
                      <i className={urgenciaStyle.icon}></i>
                      {urgenciaStyle.label}
                    </span>
                    <span className="c-muted">La urgencia será evaluada por el equipo coordinador.</span>
                  </div>

                  <button type="submit" className="btn btn-primary w-100 mt-3">
                    <i className="bi bi-send-fill me-2"></i>Enviar reporte
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
