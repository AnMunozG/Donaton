import { useState } from "react";

function calcProgreso(logro, stats) {
  switch (logro.codigo) {
    case "primera_donacion": return Math.min(100, (stats.total_donaciones / 1) * 100);
    case "corazon_solidario": return Math.min(100, (stats.total_donaciones / 5) * 100);
    case "angel_guardian": return Math.min(100, (stats.total_donaciones / 10) * 100);
    case "explorador": return Math.min(100, (stats.centros_distintos / 3) * 100);
    case "donaton_pro": return Math.min(100, (stats.centros_distintos / 5) * 100);
    case "peso_pesado": return Math.min(100, stats.total_kg);
    case "manos_abiertas": return Math.min(100, stats.total_kg / 5);
    case "multi_item": return Math.min(100, (stats.max_items_una_donacion / 3) * 100);
    default: return 0;
  }
}

function descRequisito(codigo, stats) {
  switch (codigo) {
    case "primera_donacion": return `${stats.total_donaciones} / 1 donaci\u00f3n`;
    case "corazon_solidario": return `${stats.total_donaciones} / 5 donaciones`;
    case "angel_guardian": return `${stats.total_donaciones} / 10 donaciones`;
    case "explorador": return `${stats.centros_distintos} / 3 centros`;
    case "donaton_pro": return `${stats.centros_distintos} / 5 centros`;
    case "peso_pesado": return `${stats.total_kg.toFixed(0)} / 100 kg`;
    case "manos_abiertas": return `${stats.total_kg.toFixed(0)} / 500 kg`;
    case "multi_item": return `${stats.max_items_una_donacion} / 3 items`;
    default: return "";
  }
}

export default function LogrosModal({ todosLogros, logrosIds, stats, onClose }) {
  const [filtro, setFiltro] = useState("todos");

  const obtenidos = todosLogros.filter((l) => logrosIds.has(l.id));
  const pendientes = todosLogros.filter((l) => !logrosIds.has(l.id));

  const lista = filtro === "obtenidos" ? obtenidos
    : filtro === "pendientes" ? pendientes
    : todosLogros;

  return (
    <>
      <div className="modal-backdrop fade show" onClick={onClose}></div>
      <div className="modal fade show d-block" tabIndex="-1" role="dialog">
        <div className="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header border-0 pb-0">
              <h5 className="modal-title fw-bold">
                <i className="bi bi-trophy-fill me-2 c-warning"></i>Todos los logros
              </h5>
              <button type="button" className="btn-close" onClick={onClose}></button>
            </div>
            <div className="modal-body pt-2">
              <div className="btn-group btn-group-sm mb-3 w-100">
                <button className={`btn ${filtro === "todos" ? "btn-accent" : "btn-outline-accent"}`} onClick={() => setFiltro("todos")}>
                  Todos ({todosLogros.length})
                </button>
                <button className={`btn ${filtro === "obtenidos" ? "btn-accent" : "btn-outline-accent"}`} onClick={() => setFiltro("obtenidos")}>
                  Obtenidos ({obtenidos.length})
                </button>
                <button className={`btn ${filtro === "pendientes" ? "btn-accent" : "btn-outline-accent"}`} onClick={() => setFiltro("pendientes")}>
                  Pendientes ({pendientes.length})
                </button>
              </div>

              <div className="d-flex flex-column gap-2">
                {lista.map((l) => {
                  const obtenido = logrosIds.has(l.id);
                  const progreso = calcProgreso(l, stats);
                  return (
                    <div key={l.id} className={`p-3 rounded-3 ${obtenido ? "bg-success bg-opacity-10 border border-success border-opacity-25" : "bg-page"}`}>
                      <div className="d-flex align-items-center gap-3">
                        <i className={`${l.icono} fs-3 ${obtenido ? "c-success" : "c-muted"}`}></i>
                        <div className="flex-grow-1 min-w-0">
                          <div className="d-flex align-items-center gap-2">
                            <span className="fw-semibold small">{l.nombre}</span>
                            {obtenido && <i className="bi bi-check-circle-fill c-success small"></i>}
                          </div>
                          <div className="smaller c-muted text-truncate">{l.descripcion}</div>
                          <div className="mt-2">
                            <div className="d-flex justify-content-between smaller c-muted mb-1">
                              <span>{descRequisito(l.codigo, stats)}</span>
                              <span>{Math.round(progreso)}%</span>
                            </div>
                            <div className="progress progress-thin">
                              <div className={`progress-bar ${obtenido ? "bg-success" : progreso > 0 ? "bg-warning" : ""}`}
                                role="progressbar" style={{ width: `${Math.min(100, progreso)}%` }}
                                aria-valuenow={Math.round(progreso)} aria-valuemin="0" aria-valuemax="100">
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
                {lista.length === 0 && (
                  <p className="text-center c-muted small my-4">No hay logros en esta categor&iacute;a.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}