import { useState, useEffect, useRef } from "react";
import { useBlocker } from "react-router-dom";
import { getTiposRecurso, getUnidadesPorTipo, getCamposPorTipo, getCentros, crearDonacionMultiItem } from "../api.js";
import RichTextEditor from "../componentes/RichTextEditor";
import { validarRut, validarRequerido, validarEnteroPositivo, validarForm, formatearRut, limpiarRut, capacidadColor } from "../componentes/Validaciones.js";
import donacionImg from "../assets/Donacion(6).jpg";

const EMPTY_ITEM = { tipo: "", cantidad: "", unidad: "", detalles: {}, pagado: false };

export default function Donacion() {
  const [tiposRecurso, setTiposRecurso] = useState([]);
  const [unidadesPorTipo, setUnidadesPorTipo] = useState({});
  const [camposPorTipo, setCamposPorTipo] = useState({});
  const [centros, setCentros] = useState([]);

  const [form, setForm] = useState({
    tipoOrigen: "persona", origen: "", centroId: "", notas: "",
    direccion: "", direccionDetalle: "", fechaRetiro: "",
    modoRetiro: "retiro", contactoEmail: "", contactoTel: "", enNombreDe: "",
  });
  const [items, setItems] = useState([{ ...EMPTY_ITEM }]);
  const [activeIdx, setActiveIdx] = useState(0);
  const [enviado, setEnviado] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const enviadoTimer = useRef(null);
  const removeConfirmIdx = useRef(null);

  const anyPagado = items.some((i) => i.pagado);

  useEffect(() => {
    return () => clearTimeout(enviadoTimer.current);
  }, []);

  useEffect(() => {
    if (!anyPagado) return;
    const handler = (e) => { e.preventDefault(); e.returnValue = ""; };
    window.addEventListener("beforeunload", handler);
    return () => window.removeEventListener("beforeunload", handler);
  }, [anyPagado]);

  const blocker = useBlocker(
    ({ currentLocation, nextLocation }) => anyPagado && currentLocation.pathname !== nextLocation.pathname
  );

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

  const anyNoMonetario = items.some((i) => i.tipo && i.tipo !== "Donación Monetaria");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    if (formErrors[e.target.name]) setFormErrors({ ...formErrors, [e.target.name]: "" });
  };

  const handleItemChange = (idx, field, value) => {
    setItems((prev) => {
      const next = [...prev];
      if (field === "tipo") {
        const unidades = unidadesPorTipo[value] || [];
        next[idx] = { tipo: value, cantidad: prev[idx].cantidad, unidad: unidades[0] || "", detalles: {}, pagado: false };
      } else if (field === "detalles") {
        next[idx] = { ...next[idx], detalles: { ...next[idx].detalles, ...value } };
      } else {
        next[idx] = { ...next[idx], [field]: value };
      }
      return next;
    });
  };

  const addItem = () => {
    setItems((prev) => [...prev, { ...EMPTY_ITEM }]);
    setActiveIdx(items.length);
  };

  const handleRemoveClick = (idx) => {
    if (removeConfirmIdx.current === idx) {
      removeConfirmIdx.current = null;
      setItems((prev) => {
        const next = prev.filter((_, i) => i !== idx);
        if (next.length === 0) next.push({ ...EMPTY_ITEM });
        return next;
      });
      setActiveIdx((prev) => Math.min(prev, items.length - 2));
    } else {
      removeConfirmIdx.current = idx;
      setTimeout(() => { removeConfirmIdx.current = null; }, 3000);
    }
  };

  const validarFormulario = () => {
    const reglas = [
      { campo: "origen", nombre: "RUT", validaciones: [validarRequerido, validarRut] },
      { campo: "centroId", nombre: "Centro de acopio", validaciones: [validarRequerido] },
    ];
    if (anyNoMonetario && form.modoRetiro === "retiro") {
      reglas.push(
        { campo: "direccion", nombre: "Dirección de retiro", validaciones: [validarRequerido] },
        { campo: "fechaRetiro", nombre: "Fecha de retiro", validaciones: [validarRequerido] },
      );
    }
    items.forEach((item, i) => {
      if (!item.tipo) reglas.push({ campo: `item_${i}_tipo`, nombre: `Item ${i + 1} - Tipo`, validaciones: [validarRequerido] });
      if (!item.cantidad || item.cantidad <= 0) reglas.push({ campo: `item_${i}_cantidad`, nombre: `Item ${i + 1} - Cantidad`, validaciones: [validarRequerido] });
      if (!item.unidad) reglas.push({ campo: `item_${i}_unidad`, nombre: `Item ${i + 1} - Unidad`, validaciones: [validarRequerido] });
    });
    const errores = validarForm(form, reglas);
    setFormErrors(errores);
    return Object.keys(errores).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validarFormulario()) return;

    try {
      const detalles = {};
      if (form.modoRetiro) detalles.modoRetiro = form.modoRetiro;
      if (form.contactoEmail) detalles.contactoEmail = form.contactoEmail;
      if (form.contactoTel) detalles.contactoTel = form.contactoTel;
      if (form.enNombreDe) detalles.enNombreDe = form.enNombreDe;

      await crearDonacionMultiItem({
        items: items.map((item) => {
          const tipoFinal = item.tipo === "Otros" && item.detalles?.tipoPersonalizado
            ? `Otros - ${item.detalles.tipoPersonalizado}`
            : item.tipo;
          return {
            tipo: tipoFinal,
            cantidad: item.cantidad,
            unidad: item.unidad,
            detalles: item.detalles,
          };
        }),
        origen: form.origen,
        centroId: form.centroId,
        fecha: new Date().toISOString().split("T")[0],
        notas: form.notas,
        detalles,
        direccion_retiro: anyNoMonetario && form.modoRetiro === "retiro"
          ? form.direccionDetalle
            ? `${form.direccion}, ${form.direccionDetalle}`
            : form.direccion
          : "",
        fecha_retiro: anyNoMonetario && form.modoRetiro === "retiro" ? form.fechaRetiro : "",
      });

      setEnviado(true);
      setFormErrors({});
      clearTimeout(enviadoTimer.current);
      enviadoTimer.current = setTimeout(() => setEnviado(false), 4000);
      setForm({ tipoOrigen: "persona", origen: "", centroId: "", notas: "", direccion: "", direccionDetalle: "", fechaRetiro: "", modoRetiro: "retiro", contactoEmail: "", contactoTel: "", enNombreDe: "" });
      setItems([{ ...EMPTY_ITEM }]);
      setActiveIdx(0);
    } catch {
      alert("Error al registrar la donación. Intente nuevamente.");
    }
  };

  const item = items[activeIdx] || EMPTY_ITEM;
  const unidadesDisponibles = unidadesPorTipo[item.tipo] || [];
  const camposAdicionales = camposPorTipo[item.tipo] || [];

  return (
    <div className="donacion">
      <div className="content-surface">
        <div className="d-flex flex-wrap align-items-center justify-content-between mb-4 gap-3">
          <div>
            <h1 className="fw-bold mb-1">Gestión de Donaciones</h1>
            <p className="m-0 c-muted">Registra tu donación con uno o varios artículos.</p>
          </div>
        </div>

        <div className="row g-4">
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
                {/* ── Common fields ── */}
                <div className="row g-3 mb-3">
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
                    <input type="text" name="origen" className={`form-control${formErrors.origen ? " is-invalid" : ""}`}
                      placeholder="12.345.678-K" value={formatearRut(form.origen)}
                      onChange={(e) => { const raw = limpiarRut(e.target.value); setForm({ ...form, origen: raw }); if (formErrors.origen) setFormErrors({ ...formErrors, origen: "" }); }} />
                    {formErrors.origen && <div className="invalid-feedback d-block">{formErrors.origen}</div>}
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-semibold small">Email de contacto</label>
                    <input type="email" name="contactoEmail" className="form-control"
                      placeholder="correo@ejemplo.cl" value={form.contactoEmail} onChange={handleChange} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label fw-semibold small">Teléfono de contacto</label>
                    <input type="tel" name="contactoTel" className="form-control"
                      placeholder="+56 9 1234 5678" value={form.contactoTel} onChange={handleChange} />
                  </div>
                </div>

                {/* ── Items carousel ── */}
                <div className="mt-3">
                  <label className="form-label fw-semibold small mb-2">Artículos</label>

                  {/* ── Active item form ── */}
                  <div className="p-3 rounded-3 bg-page b-card">
                    <div className="d-flex justify-content-between align-items-center mb-2">
                      <h3 className="fs-6 fw-bold mb-0 c-heading">
                        <i className="bi bi-box-seam me-1 c-primary"></i>
                        Artículo {activeIdx + 1}
                      </h3>
                      {items.length > 1 && (
                        removeConfirmIdx.current === activeIdx
                          ? (
                            <span className="small text-danger fw-semibold">
                              <i className="bi bi-exclamation-triangle me-1"></i>
                              ¿Eliminar? <button type="button" className="btn btn-sm btn-outline-danger py-0 px-2 ms-1" onClick={() => handleRemoveClick(activeIdx)}>Sí</button>
                              <button type="button" className="btn btn-sm btn-outline-secondary py-0 px-2 ms-1" onClick={() => { removeConfirmIdx.current = null; }}>No</button>
                            </span>
                          )
                          : (
                            <button type="button" className="btn btn-sm btn-outline-danger py-0 px-2"
                              onClick={() => handleRemoveClick(activeIdx)} title="Eliminar artículo">
                              <i className="bi bi-trash3"></i>
                            </button>
                          )
                      )}
                    </div>

                    <div className="row g-3">
                      <div className="col-md-6">
                        <label className="form-label fw-semibold small">Tipo de recurso</label>
                        <select className={`form-select${formErrors[`item_${activeIdx}_tipo`] ? " is-invalid" : ""}`}
                          value={item.tipo} onChange={(e) => handleItemChange(activeIdx, "tipo", e.target.value)}>
                          <option value="">Selecciona un tipo...</option>
                          {tiposRecurso.map((t) => <option key={t}>{t}</option>)}
                        </select>
                        {item.tipo === "Otros" && (
                          <div className="mt-2">
                            <label className="form-label fw-semibold small">Nombre del tipo personalizado</label>
                            <input type="text" className="form-control form-control-sm" placeholder="Ej: Equipo médico, juguetes..."
                              value={item.detalles?.tipoPersonalizado || ""}
                              onChange={(e) => handleItemChange(activeIdx, "detalles", { tipoPersonalizado: e.target.value })} />
                          </div>
                        )}
                        {formErrors[`item_${activeIdx}_tipo`] && <div className="invalid-feedback d-block">{formErrors[`item_${activeIdx}_tipo`]}</div>}
                      </div>

                      <div className="col-md-6">
                        <label className="form-label fw-semibold small">Cantidad</label>
                        <div className="input-group">
                          <input type="number" className={`form-control${formErrors[`item_${activeIdx}_cantidad`] ? " is-invalid" : ""}`}
                            placeholder="Ej: 10" min="1" step="1" value={item.cantidad}
                            onChange={(e) => handleItemChange(activeIdx, "cantidad", e.target.value)}
                            onKeyDown={(e) => { if (["." , "," , "e", "E", "-"].includes(e.key)) e.preventDefault(); }} />
                          <select className={`form-select small-form-select-width${formErrors[`item_${activeIdx}_unidad`] ? " is-invalid" : ""}`}
                            value={item.unidad} onChange={(e) => handleItemChange(activeIdx, "unidad", e.target.value)}
                            disabled={!item.tipo}>
                            {unidadesDisponibles.map((u) => <option key={u} value={u}>{u}</option>)}
                          </select>
                        </div>
                        {formErrors[`item_${activeIdx}_cantidad`] && <div className="invalid-feedback d-block">{formErrors[`item_${activeIdx}_cantidad`]}</div>}
                        {formErrors[`item_${activeIdx}_unidad`] && <div className="invalid-feedback d-block">{formErrors[`item_${activeIdx}_unidad`]}</div>}
                      </div>
                    </div>

                    {/* ── Campos adicionales per item ── */}
                    {item.tipo === "Donación Monetaria" ? (
                      <div className="mt-3 p-3 rounded-3 bg-page b-card">
                        <h4 className="fs-6 fw-bold mb-2 c-heading">
                          <i className="bi bi-credit-card-fill me-2 c-primary"></i>
                          Pago
                        </h4>
                        {!item.pagado ? (
                          <div>
                            <p className="small c-muted mb-2"><i className="bi bi-hourglass-split me-1"></i>Comprobando pago...</p>
                            <button type="button" className="btn btn-success"
                              onClick={() => { if (item.cantidad) handleItemChange(activeIdx, "pagado", true); }}
                              disabled={!item.cantidad}>
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
                        <h4 className="fs-6 fw-bold mb-2 c-heading">
                          <i className="bi bi-info-circle-fill me-2 c-primary"></i>
                          Detalles adicionales
                        </h4>
                        <div className="row g-2">
                          {camposAdicionales.map((campo) => (
                            <div key={campo.name} className="col-md-6">
                              <label className="form-label fw-semibold small">{campo.label}</label>
                              {campo.type === "select" ? (
                                <select className="form-select form-select-sm" value={item.detalles[campo.name] || ""}
                                  onChange={(e) => handleItemChange(activeIdx, "detalles", { [campo.name]: e.target.value })}>
                                  <option value="">Selecciona...</option>
                                  {campo.options.map((opt) => <option key={opt} value={opt}>{opt}</option>)}
                                </select>
                              ) : campo.type === "textarea" ? (
                                <RichTextEditor content={item.detalles[campo.name] || ""}
                                  onChange={(value) => handleItemChange(activeIdx, "detalles", { [campo.name]: value })}
                                  placeholder={`Escribe ${campo.label.toLowerCase()}...`} />
                              ) : (
                                <input type={campo.type === "date" ? "date" : "text"}
                                  className="form-control form-control-sm" placeholder={campo.placeholder || ""}
                                  value={item.detalles[campo.name] || ""}
                                  onChange={(e) => handleItemChange(activeIdx, "detalles", { [campo.name]: e.target.value })} />
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  {/* ── Carousel navigation below item form ── */}
                  <div className="d-flex align-items-center gap-1 mt-3 w-100">
                    <button type="button" className="btn btn-sm btn-outline-secondary flex-shrink-0" disabled={activeIdx === 0}
                      onClick={() => setActiveIdx((i) => i - 1)}>
                      <i className="bi bi-chevron-left"></i>
                    </button>

                    <div className="d-flex align-items-center gap-1 overflow-x-auto flex-fill-auto">
                      {items.map((_, i) => (
                        <button key={i} type="button"
                          className={`btn btn-sm rounded-circle flex-shrink-0 p-0 d-flex align-items-center justify-content-center w-32 h-32
                            ${i === activeIdx ? "btn-primary" : i === removeConfirmIdx.current ? "btn-danger" : "btn-outline-secondary"}`}
                          onClick={() => { removeConfirmIdx.current = null; setActiveIdx(i); }}>
                          {i + 1}
                        </button>
                      ))}
                      <button type="button" className="btn btn-sm btn-outline-success rounded-circle flex-shrink-0 d-flex align-items-center justify-content-center w-32 h-32" onClick={addItem} title="Agregar artículo">
                        <i className="bi bi-plus-lg"></i>
                      </button>
                    </div>

                    <button type="button" className="btn btn-sm btn-outline-secondary flex-shrink-0" disabled={activeIdx === items.length - 1}
                      onClick={() => setActiveIdx((i) => i + 1)}>
                      <i className="bi bi-chevron-right"></i>
                    </button>
                  </div>
                </div>

                {/* ── Modo de entrega (si hay item no monetario) ── */}
                {anyNoMonetario && (
                  <div className="mt-3 p-3 rounded-3 bg-page b-card">
                    <label className="form-label fw-semibold small mb-2">Modo de entrega</label>
                    <div className="d-flex flex-wrap gap-3">
                      <label className="d-flex align-items-center gap-2 form-check-label">
                        <input type="radio" name="modoRetiro" className="form-check-input"
                          value="retiro" checked={form.modoRetiro === "retiro"}
                          onChange={handleChange} />
                        <span><i className="bi bi-truck me-1 c-primary"></i>Lo retiran en mi domicilio</span>
                      </label>
                      <label className="d-flex align-items-center gap-2 form-check-label">
                        <input type="radio" name="modoRetiro" className="form-check-input"
                          value="entrega" checked={form.modoRetiro === "entrega"}
                          onChange={handleChange} />
                        <span><i className="bi bi-shop me-1 c-accent"></i>Lo llevo al centro de acopio</span>
                      </label>
                    </div>
                  </div>
                )}

                {/* ── Dirección y fecha de retiro (solo si modo retiro) ── */}
                {anyNoMonetario && form.modoRetiro === "retiro" && (
                  <div className="row g-3 mt-2">
                    <div className="col-md-8">
                      <label className="form-label fw-semibold small">Dirección de retiro</label>
                      <input type="text" name="direccion" className={`form-control${formErrors.direccion ? " is-invalid" : ""}`}
                        placeholder="Calle, número, comuna" value={form.direccion} onChange={handleChange} />
                      {formErrors.direccion && <div className="invalid-feedback d-block">{formErrors.direccion}</div>}
                    </div>
                    <div className="col-md-4">
                      <label className="form-label fw-semibold small">Detalle</label>
                      <input type="text" name="direccionDetalle" className="form-control"
                        placeholder="Depto, villa, block..." value={form.direccionDetalle} onChange={handleChange} />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label fw-semibold small">Fecha de retiro</label>
                      <input type="date" name="fechaRetiro" className={`form-control${formErrors.fechaRetiro ? " is-invalid" : ""}`}
                        value={form.fechaRetiro} onChange={handleChange} />
                      {formErrors.fechaRetiro && <div className="invalid-feedback d-block">{formErrors.fechaRetiro}</div>}
                    </div>
                  </div>
                )}

                {/* ── Centro destino ── */}
                <div className="mt-3">
                  <label className="form-label fw-semibold small">Centro de acopio destino</label>
                  <select name="centroId" className={`form-select${formErrors.centroId ? " is-invalid" : ""}`}
                    value={form.centroId} onChange={handleChange}>
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
                    const color = capacidadColor(pct);
                    return (
                      <div className="mt-2 small p-2 rounded-3 bg-page b-card">
                        <i className="bi bi-geo-alt-fill me-1 c-accent"></i>
                        {centro.direccion}
                        <div className="mt-1 d-flex align-items-center gap-2">
                          <div className="progress flex-grow-1 progress-height-6">
                            <div className="progress-bar progress-bar-rounded progress-dynamic-bar" style={{ '--bar-w': `${pct}%`, '--bar-color': color }}></div>
                          </div>
                          <span className="c-muted">{pct}% ocupado</span>
                        </div>
                      </div>
                    );
                  })()}
                </div>

                {/* ── Donación en nombre de ── */}
                <div className="mt-3">
                  <label className="form-label fw-semibold small">Donación en nombre de <span className="c-muted fw-normal">(opcional)</span></label>
                  <input type="text" name="enNombreDe" className="form-control"
                    placeholder="Ej: En memoria de un ser querido, homenaje a..." value={form.enNombreDe} onChange={handleChange} />
                </div>

                {/* ── Notas ── */}
                <div className="mt-3">
                  <label className="form-label fw-semibold small">Observaciones</label>
                  <RichTextEditor content={form.notas} onChange={(value) => setForm({ ...form, notas: value })}
                    placeholder="Escribe observaciones adicionales..." />
                </div>

                <button type="submit" className="btn btn-primary w-100 mt-3">
                  <i className="bi bi-send-fill me-2"></i>Registrar donación
                  {items.length > 1 && ` (${items.length} artículos)`}
                </button>

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
              </form>
            </div>
          </div>

          <div className="col-12 col-lg-5">
            <div className="img-placeholder rounded-4" style={{ backgroundImage: `url("${donacionImg}")` }}></div>
          </div>
        </div>
      </div>
    </div>
  );
}
