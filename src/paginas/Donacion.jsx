import { useState, useEffect } from "react";
import { useBlocker } from "react-router-dom";
import { getTiposRecurso, getUnidadesPorTipo, getCamposPorTipo, getCentros, crearDonacion } from "../api.js";
import RichTextEditor from "../componentes/RichTextEditor";
import { validarRut, validarRequerido, validarEnteroPositivo, validarForm, formatearRut, limpiarRut } from "../componentes/Validaciones.js";

export default function Donacion() {
  const [tiposRecurso, setTiposRecurso] = useState([]);
  const [unidadesPorTipo, setUnidadesPorTipo] = useState({});
  const [camposPorTipo, setCamposPorTipo] = useState({});
  const [centros, setCentros] = useState([]);

  const [form, setForm] = useState({
    tipo: "", cantidad: "", unidad: "", origen: "", tipoOrigen: "persona",
    centroId: "", notas: "", detalles: {},
    direccion: "", direccionDetalle: "", fechaRetiro: "",
  });
  const [enviado, setEnviado] = useState(false);
  const [pagado, setPagado] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  const validarFormulario = () => {
    const reglas = [
      { campo: "origen", nombre: "RUT", validaciones: [validarRequerido, validarRut] },
      { campo: "tipo", nombre: "Tipo de recurso", validaciones: [validarRequerido] },
      { campo: "cantidad", nombre: "Cantidad", validaciones: [validarRequerido, validarEnteroPositivo] },
      { campo: "unidad", nombre: "Unidad", validaciones: [validarRequerido] },
      { campo: "centroId", nombre: "Centro de acopio", validaciones: [validarRequerido] },
    ];
    if (form.tipo && form.tipo !== "Donación Monetaria") {
      reglas.push(
        { campo: "direccion", nombre: "Dirección de retiro", validaciones: [validarRequerido] },
        { campo: "fechaRetiro", nombre: "Fecha de retiro", validaciones: [validarRequerido] },
      );
    }
    const errores = validarForm(form, reglas);
    setFormErrors(errores);
    return Object.keys(errores).length === 0;
  };

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const recurso = params.get("recurso");
    const cantidadParam = params.get("cantidad");
    const unidadParam = params.get("unidad");
    const centroIdParam = params.get("centroId");

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
      if (recurso) {
        const match = tipos.includes(recurso);
        if (match) {
          const unidades = uMap[recurso] || [];
          setForm({
            tipo: recurso,
            cantidad: cantidadParam || "",
            unidad: unidadParam || (unidades[0] || ""),
            centroId: centroIdParam || "",
            origen: "",
            tipoOrigen: "persona",
            notas: "",
            detalles: {},
          });
        } else {
          setForm((prev) => ({
            ...prev,
            cantidad: cantidadParam || prev.cantidad,
            unidad: unidadParam || prev.unidad,
            centroId: centroIdParam || prev.centroId,
          }));
        }
      }
    });
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (formErrors[e.target.name]) setFormErrors({ ...formErrors, [e.target.name]: "" });
  };

  const handleTipoChange = (e) => {
    const nuevoTipo = e.target.value;
    const unidades = unidadesPorTipo[nuevoTipo] || [];
    setForm({ ...form, tipo: nuevoTipo, unidad: unidades[0] || "", detalles: {} });
    const errs = { ...formErrors };
    delete errs.tipo;
    delete errs.direccion;
    delete errs.fechaRetiro;
    setFormErrors(errs);
  };

  const handleDetalleChange = (name, value) => {
    setForm({ ...form, detalles: { ...form.detalles, [name]: value } });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validarFormulario()) return;
    crearDonacion({
      tipo: form.tipo,
      cantidad: form.cantidad,
      unidad: form.unidad,
      origen: form.origen,
      tipoOrigen: form.tipoOrigen,
      centroId: form.centroId,
      notas: form.notas,
      detalles: form.detalles,
      direccion: form.direccion,
      direccionDetalle: form.direccionDetalle,
      fechaRetiro: form.fechaRetiro,
      fecha: new Date().toISOString().split("T")[0],
    });
    setEnviado(true);
    setPagado(false);
    setFormErrors({});
    setTimeout(() => setEnviado(false), 4000);
    setForm({ tipo: "", cantidad: "", unidad: "", origen: "", tipoOrigen: "persona", centroId: "", notas: "", detalles: {}, direccion: "", direccionDetalle: "", fechaRetiro: "" });
  };

  useEffect(() => {
    if (!pagado) return;
    const handler = (e) => { e.preventDefault(); e.returnValue = ""; };
    window.addEventListener("beforeunload", handler);
    return () => window.removeEventListener("beforeunload", handler);
  }, [pagado]);

  const blocker = useBlocker(
    ({ currentLocation, nextLocation }) => pagado && currentLocation.pathname !== nextLocation.pathname
  );

  const unidadesDisponibles = unidadesPorTipo[form.tipo] || [];
  const camposAdicionales = camposPorTipo[form.tipo] || [];

  return (
    <div className="donacion">
      <div className="content-surface">

      {/* HEADER */}
      <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
        <div>
          <h1 className="fw-bold mb-1">Gestión de Donaciones</h1>
          <p className="m-0 c-muted">Registra tu donación y haz seguimiento del flujo completo.</p>
        </div>
      </div>

      <div className="row g-4">

        {/* FORMULARIO */}
        <div className="col-12 col-lg-7">
          <div className="p-4 rounded-4 card-surface">
            <h2 className="fw-bold mb-3 fs-5 c-heading">
              <i className="bi bi-gift-fill me-2 c-primary"></i>
              Nueva donación
            </h2>

            {enviado && (
              <div className="alert alert-success d-flex align-items-center gap-2 small py-2">
                <i className="bi bi-check-circle-fill"></i>
                ¡Donación registrada exitosamente!
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                <div className="col-md-6">
                  <label className="form-label fw-semibold small">Tipo de donante</label>
                  <select name="tipoOrigen" className="form-select" value={form.tipoOrigen} onChange={handleChange}>
                    <option value="persona">Persona particular</option>
                    <option value="empresa">Empresa</option>
                    <option value="municipalidad">Municipalidad</option>
                  </select>
                </div>

                <div className="col-md-6">
                  <label className="form-label fw-semibold small">RUT (sin puntos ni guion)</label>
                  <input type="text" name="origen" className={`form-control${formErrors.origen ? " is-invalid" : ""}`} placeholder="12.345.678-K" value={formatearRut(form.origen)} onChange={(e) => { const raw = limpiarRut(e.target.value); setForm({ ...form, origen: raw }); if (formErrors.origen) setFormErrors({ ...formErrors, origen: "" }); }} />
                  {formErrors.origen && <div className="invalid-feedback d-block">{formErrors.origen}</div>}
                </div>

                <div className="col-md-6">
                  <label className="form-label fw-semibold small">Tipo de recurso</label>
                  <select name="tipo" className={`form-select${formErrors.tipo ? " is-invalid" : ""}`} value={form.tipo} onChange={handleTipoChange} disabled={pagado}>
                    <option value="">Selecciona un tipo...</option>
                    {tiposRecurso.map((t) => <option key={t}>{t}</option>)}
                  </select>
                  {formErrors.tipo && <div className="invalid-feedback d-block">{formErrors.tipo}</div>}
                  {pagado && <div className="small c-accent mt-1"><i className="bi bi-lock-fill me-1"></i>Tipo bloqueado por pago</div>}
                </div>

                <div className="col-md-6">
                  <label className="form-label fw-semibold small">Cantidad</label>
                  <div className="input-group">
                    <input type="number" name="cantidad" className={`form-control${formErrors.cantidad ? " is-invalid" : ""}`} placeholder="Ej: 10" min="1" step="1" value={form.cantidad} onChange={handleChange} onKeyDown={(e) => { if (e.key === '.' || e.key === ',' || e.key === 'e' || e.key === 'E' || e.key === '-') e.preventDefault(); }} />
                    <select name="unidad" className={`form-select small-form-select-width${formErrors.unidad ? " is-invalid" : ""}`} value={form.unidad} onChange={handleChange} disabled={!form.tipo}>
                      {unidadesDisponibles.map((u) => <option key={u} value={u}>{u}</option>)}
                    </select>
                  </div>
                  {formErrors.cantidad && <div className="invalid-feedback d-block">{formErrors.cantidad}</div>}
                  {formErrors.unidad && <div className="invalid-feedback d-block">{formErrors.unidad}</div>}
                </div>
              </div>

              {/* Dirección y fecha de retiro (solo donaciones no monetarias) */}
              {form.tipo && form.tipo !== "Donación Monetaria" && (
                <div className="row g-3 mt-2">
                  <div className="col-md-8">
                    <label className="form-label fw-semibold small">Dirección de retiro</label>
                    <input type="text" name="direccion" className={`form-control${formErrors.direccion ? " is-invalid" : ""}`} placeholder="Calle, número, comuna" value={form.direccion} onChange={handleChange} disabled={pagado} />
                    {formErrors.direccion && <div className="invalid-feedback d-block">{formErrors.direccion}</div>}
                  </div>
                  <div className="col-md-4">
                    <label className="form-label fw-semibold small">Detalle</label>
                    <input type="text" name="direccionDetalle" className="form-control" placeholder="Depto, villa, block..." value={form.direccionDetalle} onChange={handleChange} disabled={pagado} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-semibold small">Fecha de retiro</label>
                    <input type="date" name="fechaRetiro" className={`form-control${formErrors.fechaRetiro ? " is-invalid" : ""}`} value={form.fechaRetiro} onChange={handleChange} disabled={pagado} />
                    {formErrors.fechaRetiro && <div className="invalid-feedback d-block">{formErrors.fechaRetiro}</div>}
                  </div>
                </div>
              )}

              {/* Campos adicionales */}
              {form.tipo === "Donación Monetaria" ? (
                <div className="mt-3 p-3 rounded-3 bg-page b-card">
                  <h3 className="fs-6 fw-bold mb-2 c-heading">
                    <i className="bi bi-credit-card-fill me-2 c-primary"></i>
                    Pago
                  </h3>
                  {!pagado ? (
                    <div>
                      <p className="small c-muted mb-2"><i className="bi bi-hourglass-split me-1"></i>Comprobando pago...</p>
                      <button type="button" className="btn btn-success" onClick={() => { if (form.cantidad) setPagado(true); }} disabled={!form.cantidad}>
                        <i className="bi bi-wallet2 me-1"></i>Ir a portal de pago
                      </button>
                    </div>
                  ) : (
                    <div className="d-flex align-items-center gap-2">
                      <i className="bi bi-check-circle-fill fs-5 c-accent"></i>
                      <span className="fw-semibold c-accent">Pagado</span>
                    </div>
                  )}
                </div>
              ) : camposAdicionales.length > 0 && (
                <div className="mt-3 p-3 rounded-3 bg-page b-card">
                  <h3 className="fs-6 fw-bold mb-2 c-heading">
                    <i className="bi bi-info-circle-fill me-2 c-primary"></i>
                    Detalles adicionales
                  </h3>
                  <div className="row g-2">
                    {camposAdicionales.map((campo) => (
                      <div key={campo.name} className="col-md-6">
                        <label className="form-label fw-semibold small">{campo.label}</label>
                        {campo.type === "select" ? (
                          <select className="form-select form-select-sm" value={form.detalles[campo.name] || ""} onChange={(e) => handleDetalleChange(campo.name, e.target.value)}>
                            <option value="">Selecciona...</option>
                            {campo.options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
                          </select>
                        ) : campo.type === "textarea" ? (
                          <RichTextEditor content={form.detalles[campo.name] || ""} onChange={(value) => handleDetalleChange(campo.name, value)} placeholder={`Escribe ${campo.label.toLowerCase()}...`} />
                        ) : (
                          <input type={campo.type === "date" ? "date" : "text"} className="form-control form-control-sm" placeholder={campo.placeholder || ""} value={form.detalles[campo.name] || ""} onChange={(e) => handleDetalleChange(campo.name, e.target.value)} />
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Centro destino */}
              <div className="mt-3">
                <label className="form-label fw-semibold small">Centro de acopio destino</label>
                <select name="centroId" className={`form-select${formErrors.centroId ? " is-invalid" : ""}`} value={form.centroId} onChange={handleChange}>
                  <option value="">Selecciona un centro...</option>
                  {centros.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.nombre} — {c.region}
                      {c.estado === "Capacidad crítica" ? " ⚠️ Capacidad crítica" : ""}
                    </option>
                  ))}
                </select>
                {formErrors.centroId && <div className="invalid-feedback d-block">{formErrors.centroId}</div>}

                {form.centroId && (() => {
                  const centro = centros.find((c) => c.id === form.centroId);
                  if (!centro) return null;
                  const pct = Math.round((centro.capacidadUsada / centro.capacidadTotal) * 100);
                  const color = pct >= 85 ? "#DD4444" : pct >= 60 ? "#FFC107" : "#3AB795";
                  return (
                    <div className="mt-2 small p-2 rounded-3 bg-page b-card">
                      <i className="bi bi-geo-alt-fill me-1 c-accent"></i>
                      {centro.direccion}
                      <div className="mt-1 d-flex align-items-center gap-2">
                        <div className="progress flex-grow-1 progress-height-6">
                          <div className="progress-bar progress-bar-rounded" style={{ width: `${pct}%`, background: color }}></div>
                        </div>
                        <span className="c-muted">{pct}% ocupado</span>
                      </div>
                    </div>
                  );
                })()}
              </div>

              {/* Notas */}
              <div className="mt-3">
                <label className="form-label fw-semibold small">Observaciones</label>
                <RichTextEditor content={form.notas} onChange={(value) => setForm({ ...form, notas: value })} placeholder="Escribe observaciones adicionales..." />
              </div>

              {blocker.state === "blocked" && (
                <div className="modal d-block modal-overlay" tabIndex="-1">
                  <div className="modal-dialog modal-dialog-centered">
                    <div className="modal-content">
                      <div className="modal-header">
                        <h5 className="modal-title">
                          <i className="bi bi-exclamation-triangle-fill me-2 c-warning"></i>
                          ¿Salir sin confirmar?
                        </h5>
                      </div>
                      <div className="modal-body">
                        <p className="mb-0">Tienes un pago registrado. Si sales perderás los datos de la donación.</p>
                      </div>
                      <div className="modal-footer">
                        <button className="btn btn-secondary" onClick={() => blocker.reset()}>Seguir aquí</button>
                        <button className="btn btn-danger" onClick={() => blocker.proceed()}>Salir de todas formas</button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <button type="submit" className="btn btn-primary w-100 mt-3">
                <i className="bi bi-send-fill me-2"></i>Registrar donación
              </button>

            </form>
          </div>
        </div>

        {/* IMAGEN LATERAL */}
        <div className="col-12 col-lg-5">
          <div className="img-placeholder rounded-4" style={{ backgroundImage: "url(https://images.squarespace-cdn.com/content/v1/618ac2f3b0b4d00cad7be26b/ff8cb020-626b-4e28-bd2a-b1bdd61799c2/FOTO+SOCIOS+ABCHILE+DONACIONES.png)" }}></div>
        </div>

      </div>
    </div>
    </div>
  );
}
