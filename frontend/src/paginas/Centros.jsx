import { useState, useEffect } from "react";
import { getCentros, getNecesidades, getRuta, urgenciaColorMap, estadoNecColorMap } from "../api.js";
import { capacidadColor } from "../componentes/Validaciones.js";
import Mapa from "../componentes/Mapa";
import banner2Img from "../assets/Banner2.png";

const TRAVEL_MODES = [
  { key: "driving",  label: "Auto",       icon: "bi-car-front" },
  { key: "walking",  label: "Caminando",  icon: "bi-person-walking" },
  { key: "cycling",  label: "Bicicleta",  icon: "bi-bicycle" },
];

export default function Centros() {
  const [centros, setCentros] = useState([]);
  const [necesidades, setNecesidades] = useState([]);
  const [seleccionado, setSeleccionado] = useState(null);
  const [filtroRegion, setFiltroRegion] = useState("Todas");
  const [routeLine, setRouteLine] = useState(null);
  const [userLocation, setUserLocation] = useState(null);
  const [routeInfo, setRouteInfo] = useState(null);
  const [routeLoading, setRouteLoading] = useState(false);
  const [routeError, setRouteError] = useState(null);
  const [travelMode, setTravelMode] = useState("driving");

  useEffect(() => {
    getCentros().then(setCentros);
    getNecesidades().then(setNecesidades);
  }, []);

  useEffect(() => {
    setRouteLine(null);
    setRouteInfo(null);
    setRouteError(null);
  }, [seleccionado]);

  const regiones = ["Todas", ...new Set(centros.map((c) => c.region))];

  const centrosFiltrados = filtroRegion === "Todas"
    ? centros
    : centros.filter((c) => c.region === filtroRegion);

  const needsActivas = necesidades.filter((n) => n.estado !== "Pendiente");
  const necesidadesDelCentro = seleccionado
    ? needsActivas.filter((n) => n.centroId === seleccionado.id)
    : [];

  function fetchRoute(origen, modo) {
    setRouteError(null);
    setRouteLoading(true);
    setRouteLine(null);
    setRouteInfo(null);

    const dest = seleccionado.coordenadas;
    if (!origen?.lat || !origen?.lng || !dest?.lat || !dest?.lng || isNaN(+origen.lat) || isNaN(+origen.lng) || isNaN(+dest.lat) || isNaN(+dest.lng)) {
      setRouteError("Coordenadas inválidas. El centro no tiene una ubicación registrada.");
      setRouteLoading(false);
      return;
    }

    getRuta(origen.lat, origen.lng, dest.lat, dest.lng, modo)
      .then((data) => {
        setRouteLine(data.line);
        setRouteInfo({ distancia: data.distancia, duracion: data.duracion });
      })
      .catch((err) => {
        const msg = err?.response?.data?.detail || err?.message || "Error al calcular la ruta";
        setRouteError(msg);
      })
      .finally(() => setRouteLoading(false));
  }

  function handleLocalizar() {
    if (!seleccionado?.coordenadas) return;

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const user = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        setUserLocation(user);
        fetchRoute(user, travelMode);
      },
      (err) => {
        setRouteError(
          err.code === 1
            ? "Permiso de ubicación denegado. Actívalo en la configuración de tu navegador."
            : "No se pudo obtener tu ubicación. Verifica que el GPS esté activo."
        );
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }

  function handleCambiarModo(modo) {
    setTravelMode(modo);
    if (userLocation) {
      fetchRoute(userLocation, modo);
    }
  }

  function limpiarRuta() {
    setRouteLine(null);
    setUserLocation(null);
    setRouteInfo(null);
    setRouteError(null);
  }

  function formatearDistancia(m) {
    if (!m) return "";
    return m >= 1000 ? `${(m / 1000).toFixed(1)} km` : `${Math.round(m)} m`;
  }

  function formatearDuracion(s) {
    if (!s) return "";
    return s >= 3600
      ? `${Math.floor(s / 3600)} h ${Math.round((s % 3600) / 60)} min`
      : `${Math.round(s / 60)} min`;
  }

  return (
    <div className="centros">

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

        <div className="col-12 col-lg-4 d-flex flex-column">
          <div className="card-surface rounded-4 p-3 d-flex flex-column gap-3 lista-centros">
            {centrosFiltrados.map((c) => {
              const pct = Math.round((c.capacidadUsada / c.capacidadTotal) * 100);
              const barColor = capacidadColor(pct);
              const necesidadesCount = needsActivas.filter((n) => n.centroId === c.id).length;

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

        <div className="col-12 col-lg-8">
          <div className="mb-3">
            <Mapa
              centros={centrosFiltrados}
              seleccionado={seleccionado}
              onSelect={setSeleccionado}
              routeLine={routeLine}
              userLocation={userLocation}
            />
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
                  <div className="small c-muted d-flex align-items-center gap-2 flex-wrap">
                    <span><i className="bi bi-geo-alt-fill me-1 c-accent"></i>{seleccionado.direccion}</span>
                    {seleccionado.coordenadas && (
                      <button
                        className="btn-localizar"
                        onClick={handleLocalizar}
                        disabled={routeLoading}
                        title="Generar ruta desde tu ubicación"
                      >
                        <i className="bi bi-pin-map"></i>
                        {routeLoading ? " Calculando..." : " Localizar"}
                      </button>
                    )}
                  </div>
                </div>
                <div className="col-6">
                  <div className="small c-muted"><i className="bi bi-person-fill me-1 c-accent"></i>Encargado/a</div>
                  <div className="fw-semibold">{seleccionado.encargado || "—"}</div>
                </div>
                <div className="col-6">
                  <div className="small c-muted"><i className="bi bi-telephone-fill me-1 c-accent"></i>Contacto</div>
                  <div className="fw-semibold">{seleccionado.telefono || "—"}</div>
                </div>
              </div>

              {routeError && (
                <div className="alert alert-warning py-2 px-3 small d-flex align-items-center gap-2 mb-4">
                  <i className="bi bi-exclamation-triangle-fill"></i>
                  {routeError}
                </div>
              )}

              {(routeInfo || userLocation) && (
                <div className="route-info d-flex align-items-start flex-column flex-sm-row align-items-sm-center justify-content-between flex-wrap gap-2 mb-4 py-2 px-3 rounded-3">
                  <div className="d-flex align-items-center gap-2 flex-wrap small">
                    {routeInfo ? (
                      <>
                        <span><i className="bi bi-geo-alt-fill me-1 text-primary"></i>Tu ubicación</span>
                        <i className="bi bi-arrow-right c-muted"></i>
                        <span><i className="bi bi-building me-1 text-success"></i>{seleccionado.nombre}</span>
                        <span className="badge bg-light text-dark border">
                          <i className="bi bi-sign-turn-right me-1"></i>{formatearDistancia(routeInfo.distancia)}
                        </span>
                        <span className="badge bg-light text-dark border">
                          <i className="bi bi-clock me-1"></i>{formatearDuracion(routeInfo.duracion)}
                        </span>
                      </>
                    ) : (
                      <span className="c-muted">
                        {routeLoading ? (
                          <><span className="spinner-border spinner-border-sm me-1" role="status"></span>Calculando ruta...</>
                        ) : (
                          <><i className="bi bi-geo-alt-fill me-1 text-primary"></i>Ubicación obtenida</>
                        )}
                      </span>
                    )}
                    <div className="btn-group btn-group-sm ms-1" role="group">
                      {TRAVEL_MODES.map((m) => (
                        <button
                          key={m.key}
                          className={`btn btn-sm ${travelMode === m.key ? "btn-primary" : "btn-outline-primary"}`}
                          onClick={() => handleCambiarModo(m.key)}
                          title={m.label}
                          disabled={routeLoading}
                        >
                          <i className={m.icon}></i>
                        </button>
                      ))}
                    </div>
                  </div>
                  <div className="d-flex gap-1">
                    <button className="btn btn-sm btn-outline-secondary" onClick={limpiarRuta}>
                      <i className="bi bi-x-lg"></i>
                    </button>
                  </div>
                </div>
              )}

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
