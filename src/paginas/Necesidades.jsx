import { useState, useEffect } from "react";
import { getTiposRecurso, getUnidadesPorTipo, getCentros } from "../api.js";
import { agregarNecesidadUsuario } from "../componentes/Datos.jsx";
import RichTextEditor from "../componentes/RichTextEditor";
import { validarRequerido, validarEnteroPositivo, validarForm } from "../componentes/Validaciones.js";

export default function Necesidades() {
  const [tiposRecurso, setTiposRecurso] = useState([]);
  const [unidadesPorTipo, setUnidadesPorTipo] = useState({});
  const [centros, setCentros] = useState([]);

  const [form, setForm] = useState({
    recurso: "", cantidad: "", unidad: "",
    descripcion: "", reportadoPor: "", centroAcopio: "",
  });
  const [enviado, setEnviado] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    getTiposRecurso().then(setTiposRecurso);
    getUnidadesPorTipo().then(setUnidadesPorTipo);
    getCentros().then(setCentros);
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (formErrors[e.target.name]) setFormErrors({ ...formErrors, [e.target.name]: "" });
  };

  const handleRecursoChange = (e) => {
    const nuevoRecurso = e.target.value;
    const unidades = unidadesPorTipo[nuevoRecurso] || [];
    setForm({ ...form, recurso: nuevoRecurso, unidad: unidades[0] || "" });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errores = validarForm(form, [
      { campo: "reportadoPor", nombre: "Reportado por", validaciones: [validarRequerido] },
      { campo: "recurso", nombre: "Recurso", validaciones: [validarRequerido] },
      { campo: "cantidad", nombre: "Cantidad", validaciones: [validarRequerido, validarEnteroPositivo] },
      { campo: "unidad", nombre: "Unidad", validaciones: [validarRequerido] },
      { campo: "centroAcopio", nombre: "Centro de acopio", validaciones: [validarRequerido] },
    ]);
    setFormErrors(errores);
    if (Object.keys(errores).length > 0) return;
    agregarNecesidadUsuario({
      recurso: form.recurso,
      cantidad: form.cantidad,
      unidad: form.unidad,
      descripcion: form.descripcion,
      reportadoPor: form.reportadoPor,
      centroId: form.centroAcopio,
      centro: centros.find((c) => c.id === form.centroAcopio)?.nombre || "",
    });
    setEnviado(true);
    setFormErrors({});
    setTimeout(() => setEnviado(false), 4000);
    setForm({ recurso: "", cantidad: "", unidad: "", descripcion: "", reportadoPor: "", centroAcopio: "" });
  };

  const unidadesDisponibles = unidadesPorTipo[form.recurso] || [];

  return (
    <div className="necesidades">
      <div className="content-surface">

      {/* HEADER */}
      <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
        <div>
          <h1 className="fw-bold mb-1">Necesidades en Terreno</h1>
          <p className="m-0 c-muted">Reporta necesidades urgentes para coordinar la ayuda de forma eficiente.</p>
        </div>
        <span className="page-header-pill warning-pill">
          <i className="bi bi-exclamation-triangle-fill"></i>Reporte directo
        </span>
      </div>

      <div className="row g-4">

        {/* IMAGEN */}
        <div className="col-12 col-lg-5">
          <div className="img-placeholder rounded-4" style={{ backgroundImage: "url(https://chile.iom.int/sites/g/files/tmzbdl906/files/coim-chile-francisca-salinas_oim-entrega-alimentos_1.jpg)" }}></div>
        </div>

        {/* FORMULARIO */}
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

            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label fw-semibold small">Reportado por</label>
                  <input type="text" name="reportadoPor" className={`form-control${formErrors.reportadoPor ? " is-invalid" : ""}`} placeholder="Municipalidad, voluntario..." value={form.reportadoPor} onChange={handleChange} />
                  {formErrors.reportadoPor && <div className="invalid-feedback d-block">{formErrors.reportadoPor}</div>}
                </div>

                <div className="col-md-6">
                  <label className="form-label fw-semibold small">Recurso necesitado</label>
                  <select name="recurso" className={`form-select${formErrors.recurso ? " is-invalid" : ""}`} value={form.recurso} onChange={handleRecursoChange}>
                    <option value="">Selecciona...</option>
                    {tiposRecurso.map((t) => <option key={t}>{t}</option>)}
                  </select>
                  {formErrors.recurso && <div className="invalid-feedback d-block">{formErrors.recurso}</div>}
                </div>

                <div className="col-md-6">
                  <label className="form-label fw-semibold small">Cantidad requerida</label>
                  <div className="input-group">
                    <input type="number" name="cantidad" className={`form-control${formErrors.cantidad ? " is-invalid" : ""}`} placeholder="Ej: 100" min="1" step="1" value={form.cantidad} onChange={handleChange} />
                    <select name="unidad" className={`form-select small-form-select-width${formErrors.unidad ? " is-invalid" : ""}`} value={form.unidad} onChange={handleChange} disabled={!form.recurso}>
                      {unidadesDisponibles.map((u) => <option key={u} value={u}>{u}</option>)}
                    </select>
                  </div>
                  {formErrors.cantidad && <div className="invalid-feedback d-block">{formErrors.cantidad}</div>}
                  {formErrors.unidad && <div className="invalid-feedback d-block">{formErrors.unidad}</div>}
                </div>

                <div className="col-md-6">
                  <label className="form-label fw-semibold small">Centro de acopio</label>
                  <select name="centroAcopio" className={`form-select${formErrors.centroAcopio ? " is-invalid" : ""}`} value={form.centroAcopio} onChange={handleChange}>
                    <option value="">Selecciona...</option>
                    {centros.map((centro) => <option key={centro.id} value={centro.id}>{centro.nombre}</option>)}
                  </select>
                  {formErrors.centroAcopio && <div className="invalid-feedback d-block">{formErrors.centroAcopio}</div>}
                </div>
              </div>

              <div className="mt-3">
                <label className="form-label fw-semibold small">Descripción</label>
                <RichTextEditor content={form.descripcion} onChange={(value) => setForm({ ...form, descripcion: value })} placeholder="Describe la necesidad en detalle..." />
              </div>

              <button type="submit" className="btn btn-primary w-100 mt-3">
                <i className="bi bi-send-fill me-2"></i>Enviar reporte
              </button>
            </form>
          </div>
        </div>

      </div>
    </div>
    </div>
  );
}
