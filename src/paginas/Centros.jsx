import { useState, useEffect } from "react";
import { getCentros, getNecesidades, urgenciaColorMap, estadoNecColorMap } from "../api.js";
import Mapa from "../componentes/Mapa";
import banner2Img from "../assets/Banner2.png";

export default function Centros() {
  const [centros, setCentros] = useState([]);
  const [necesidades, setNecesidades] = useState([]);
  const [seleccionado, setSeleccionado] = useState(null);
  const [filtroRegion, setFiltroRegion] = useState("Todas");

  useEffect(() => {
    getCentros().then(setCentros);
    getNecesidades().then(setNecesidades);
  }, []);

  const regiones = ["Todas", ...new Set(centros.map((c) => c.region))];

  const centrosFiltrados = filtroRegion === "Todas"
    ? centros
    : centros.filter((c) => c.region === filtroRegion);

  const necesidadesDelCentro = seleccionado
    ? necesidades.filter((n) => n.centroId === seleccionado.id)
    : [];

  return (
    <div className="centros">

      {/* BANNER */}
      <div className="banner-centros" style={{ backgroundImage: `url(${banner2Img})` }}>
        <div className="banner-content-wrapper">
          <span className="banner-pill banner-pill-small mb-2">
            {centros.length} CENTROS ACTIVOS
          </span>
          <h1 className="h1-banner">Centros de Acopio</h1>
          <p className="banner-text">
            Consulta la capacidad y las necesidades asignadas a cada centro de acopio activo.
          </p>
        </div>
      </div>

      <div className="content-surface">

      {/* FILTROS */}
      <div className="d-flex gap-2 flex-wrap mb-4">
        {regiones.map((r) => (
          <button key={r}
            className={`filter-btn ${filtroRegion === r ? "active" : ""}`}
            onClick={() => setFiltroRegion(r)}>
            {r}
          </button>
        ))}
      </div>

      <div className="row g-4">

        {/* LISTA */}
        <div className="col-12 col-lg-4 d-flex flex-column">
          <div className="card-surface rounded-4 p-3 d-flex flex-column gap-3 lista-centros">
            {centrosFiltrados.map((c) => {
              const pct = Math.round((c.capacidadUsada / c.capacidadTotal) * 100);
              const barColor = pct >= 85 ? "#DD4444" : pct >= 60 ? "#FFC107" : "#3AB795";
              const necesidadesCount = necesidades.filter((n) => n.centroId === c.id).length;

              return (
                <div key={c.id}
                  className={`center-card ${seleccionado?.id === c.id ? "selected" : ""}`}
                  onClick={() => setSeleccionado(seleccionado?.id === c.id ? null : c)}>

                  <div className="d-flex justify-content-between align-items-start mb-2">
                    <div>
                      <div className="d-flex align-items-center gap-2 mb-1">
                        <span className="center-id">{c.id}</span>
                        <span className="center-percent"
                          style={{ background: barColor + "18", color: barColor }}>{pct}%</span>
                      </div>
                      <div className="center-name">{c.nombre}</div>
                      <div className="small c-muted">
                        <i className="bi bi-geo-alt-fill me-1 c-accent"></i>{c.region}
                      </div>
                    </div>
                    <div className="d-flex flex-column align-items-end gap-1 flex-shrink-0">
                      <span className={`badge ${c.estado === "Activo" ? "bg-success" : "bg-danger"}`}>{c.estado}</span>
                      {necesidadesCount > 0 && (
                        <span className="needs-badge">
                          <i className="bi bi-flag-fill"></i>{necesidadesCount} neces.
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="small d-flex justify-content-between mb-1">
                    <span className="c-muted">Capacidad usada</span>
                    <span className="center-capacity-text">{c.capacidadUsada.toLocaleString()} / {c.capacidadTotal.toLocaleString()} kg</span>
                  </div>

                  <div className="progress progress-height-6">
                    <div className="progress-bar progress-bar-rounded" style={{ width: `${pct}%`, background: barColor }}></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* MAPA + DETALLE */}
        <div className="col-12 col-lg-8">
          <div className="mb-3">
            <Mapa centros={centrosFiltrados} seleccionado={seleccionado} onSelect={setSeleccionado} />
          </div>

          {seleccionado ? (
            <div className="p-4 rounded-4 card-surface">
              <div className="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                <div>
                  <span className="center-id">{seleccionado.id}</span>
                  <h2 className="fw-bold fs-5 mb-0 c-heading">{seleccionado.nombre}</h2>
                </div>
                <span className={`badge ${seleccionado.estado === "Activo" ? "bg-success" : "bg-danger"}`}>{seleccionado.estado}</span>
              </div>

              <div className="row g-3 mb-4">
                <div className="col-12">
                  <div className="small c-muted">
                    <i className="bi bi-geo-alt-fill me-1 c-accent"></i>{seleccionado.direccion}
                  </div>
                </div>
                <div className="col-6">
                  <div className="small c-muted"><i className="bi bi-person-fill me-1 c-accent"></i>Encargado/a</div>
                  <div className="fw-semibold">{seleccionado.encargado}</div>
                </div>
                <div className="col-6">
                  <div className="small c-muted"><i className="bi bi-telephone-fill me-1 c-accent"></i>Contacto</div>
                  <div className="fw-semibold">{seleccionado.telefono}</div>
                </div>
              </div>

              <h3 className="fs-6 fw-bold mb-3 c-heading">
                <i className="bi bi-flag-fill me-2 c-primary"></i>Necesidades asignadas
              </h3>

              {necesidadesDelCentro.length === 0 ? (
                <div className="center-no-needs">
                  <i className="bi bi-check-circle-fill c-accent"></i>
                  <span className="small c-muted">No hay necesidades asignadas a este centro actualmente.</span>
                </div>
              ) : (
                <div className="d-flex flex-column gap-2 needs-scroll">
                  {necesidadesDelCentro.map((n) => (
                    <div key={n.id} className="p-3 rounded-3 d-flex justify-content-between align-items-start flex-wrap gap-2 bg-page b-card">
                      <div>
                        <div className="fw-semibold small c-heading">{n.recurso} — {n.cantidad} {n.unidad}</div>
                        <div className="small c-muted"><i className="bi bi-building me-1"></i>{n.centro || seleccionado?.nombre || "Sin centro"}</div>
                        <div className="small c-muted"><i className="bi bi-person me-1"></i>{n.reportadoPor}</div>
                      </div>
                      <div className="d-flex gap-1 flex-wrap">
                        <span className={`badge bg-${urgenciaColorMap[n.urgencia]}`}>{n.urgencia}</span>
                        <span className={`badge bg-${estadoNecColorMap[n.estado]}`}>{n.estado}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="center-empty-state">
              <i className="bi bi-building center-empty-icon"></i>
              <p className="c-muted">Selecciona un centro en el mapa o en la lista para ver su detalle.</p>
            </div>
          )}
        </div>
      </div>

    </div>
    </div>
  );
}
