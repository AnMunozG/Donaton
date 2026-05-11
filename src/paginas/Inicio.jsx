import { useState, useEffect } from "react";
import { DonatonLogo } from "../componentes/Logos.jsx";
import { getCategoriasDonacion, getPasosFuncionamiento, getNecesidades, getCentros } from "../api.js";
import bannerInicioImg from "../assets/BannerInicio.png";


export default function Inicio() {
  const [categorias, setCategorias] = useState([]);
  const [pasos, setPasos] = useState([]);
  const [necesidades, setNecesidades] = useState([]);
  const [centros, setCentros] = useState([]);

  useEffect(() => {
    getCategoriasDonacion().then(setCategorias);
    getPasosFuncionamiento().then(setPasos);
    getNecesidades().then(setNecesidades);
    getCentros().then(setCentros);
  }, []);

  const centroNombre = (centroId) => centros.find((c) => c.id === centroId)?.nombre || "";

  const items = [...categorias, ...categorias];
  const urgenciaPeso = { Alta: 0, Media: 1, Baja: 2 };
  const activas = necesidades
    .filter((n) => n.estado !== "Cubierto")
    .sort((a, b) => {
      const ua = urgenciaPeso[a.urgencia] ?? 99;
      const ub = urgenciaPeso[b.urgencia] ?? 99;
      if (ua !== ub) return ua - ub;
      return (Number(b.donado) / Number(b.cantidad)) - (Number(a.donado) / Number(a.cantidad));
    })
    .slice(0, 6);

  return (
    <div className="inicio">

      {/* Banner */}
      <div className="hero-banner hero-banner-pagina" style={{ backgroundImage: `url(${bannerInicioImg})` }}>
        <div className="hero-banner-content">
          <DonatonLogo variante="banner" />
          <h2>Coordinando la ayuda donde más se necesita</h2>
          <p>
            Donatón conecta a donantes, empresas, municipalidades y equipos logísticos
            para llevar ayuda humanitaria de forma transparente y eficiente a quienes más lo necesitan.
          </p>
          <div className="d-flex gap-3 justify-content-center mt-4 flex-wrap">
            <a href="/donacion" className="btn btn-primary btn-lg px-4">
              <i className="bi bi-heart-fill me-2"></i>Hacer una donación
            </a>
            <a href="/necesidades" className="btn btn-accent btn-lg px-4">
              <i className="bi bi-flag-fill me-2"></i>Reportar una necesidad
            </a>
          </div>
        </div>
      </div>

      <div className="content-surface">

      {/* Transparencia */}
      <div className="mb-5 p-4 rounded-4 b-card-accent bg-surface">
        <div className="row align-items-center">
          <div className="col-md-8">
            <h2 className="fw-bold mb-3 c-heading">
              <i className="bi bi-shield-check-fill me-2 c-accent"></i>
              Transparencia en cada donación
            </h2>
            <p className="c-muted">
              En Donatón creemos que la transparencia es fundamental. Cada donación, cada peso y cada recurso
              es rastreado y documentado. Puedes ver exactamente dónde va tu ayuda y cómo es utilizada.
            </p>
          </div>
          <div className="col-md-4 text-center text-md-end mt-3 mt-md-0">
            <a href="/transparencia" className="btn btn-accent btn-lg px-4">
              <i className="bi bi-info-circle-fill me-2"></i>Saber más
            </a>
          </div>
        </div>
      </div>

      {/* Imagen y Estadísticas */}
      <div className="row g-4 mb-5 align-items-center">
        <div className="col-md-5">
          <div className="img-placeholder rounded-4"
            style={{ backgroundImage: `url("https://www.worldvision.cl/hs-fs/hubfs/Ecuador/EC-Blog/P%C3%8DA%201.jpg?width=600&name=P%C3%8DA%201.jpg")` }}></div>
        </div>
        <div className="col-md-7">
          <div className="row row-cols-2 g-3">
            {[
              { icono: "bi-heart-fill", valor: "12.400+", texto: "Donaciones recibidas" },
              { icono: "bi-house-fill", valor: "38", texto: "Centros de acopio activos" },
              { icono: "bi-people-fill", valor: "5.200+", texto: "Familias beneficiadas" },
              { icono: "bi-truck", valor: "920", texto: "Envíos completados" },
            ].map((s, i) => (
              <div key={i} className="col">
                <div className="text-center p-3 rounded-4 h-100 card-surface">
                  <i className={`bi ${s.icono} fs-2 mb-1 c-primary`}></i>
                  <div className="fw-bold fs-4 c-primary">{s.valor}</div>
                  <div className="small c-muted">{s.texto}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Carrusel infinito e imagen */}
      <div className="row g-4 mb-5 align-items-center">
        <div className="col-md-7">
          <h2 className="fw-bold mb-1">¿Qué puedes donar?</h2>
          <p className="mb-3 c-muted">
            Aceptamos distintos tipos de recursos según las necesidades reportadas en terreno.
          </p>
          <div className="carrusel-outer m-0">
            <div className="carrusel-track">
              {items.map((cat, i) => (
                <div key={i} className="carrusel-card">
                  <i className={`bi ${cat.icon} fs-2 mb-3 d-block c-accent`}></i>
                  <div className="fw-semibold mb-1 c-heading">{cat.nombre}</div>
                  <div className="small c-muted">{cat.descripcion}</div>
                </div>
              ))}
            </div>
          </div>
          <a href="/donacion" className="btn btn-success btn-lg px-4 mt-3 d-block mx-auto btn-fit">
            <i className="bi bi-heart-fill me-1"></i>Ir a donar
          </a>
        </div>
        <div className="col-md-5">
          <div className="img-placeholder rounded-4"
            style={{ backgroundImage: "url(https://chile.iom.int/sites/g/files/tmzbdl906/files/styles/card_format/public/banner/37_0.jpg?itok=EVAQURnR)" }}></div>
        </div>
      </div>

      {/* Proyectos activos */}
      {activas.length > 0 && (
        <div className="mb-5">
          <h2 className="fw-bold mb-1">Proyectos activos</h2>
          <p className="mb-4 c-muted">Necesidades reportadas en terreno que requieren tu ayuda.</p>
          <div className="row g-3">
            {activas.map((n) => {
              const total = Number(n.cantidad);
              const donado = Number(n.donado) || 0;
              const pct = total > 0 ? Math.round((donado / total) * 100) : 0;
              const falta = total - donado;
              return (
                <div key={n.id} className="col-12 col-md-6 col-lg-4">
                  <div className="project-card">
                    <div className="d-flex align-items-start justify-content-between mb-2">
                      <span className={`badge bg-${n.urgencia === "Alta" ? "danger" : n.urgencia === "Media" ? "warning" : "secondary"}`}>
                        {n.urgencia}
                      </span>
                      <span className="project-id">{n.id}</span>
                    </div>
                    <h3 className="project-resource">{n.recurso}</h3>
                    <p className="project-goal">
                      <i className="bi bi-building me-1 c-accent"></i>{centroNombre(n.centroId) || n.centro || "Sin centro"}
                    </p>
                    {n.descripcion && (
                      <p className="project-desc small c-muted mb-2">{n.descripcion}</p>
                    )}
                    <div className="mb-2">
                      <div className="d-flex justify-content-between small mb-1">
                        <span className="c-muted">{donado} / {total} {n.unidad}</span>
                        <span className="fw-semibold" style={{ color: pct >= 80 ? "#3AB795" : pct >= 50 ? "#FFC107" : "#DD4444" }}>{pct}%</span>
                      </div>
                      <div className="progress progress-height-6">
                        <div className="progress-bar progress-bar-rounded" style={{ width: `${pct}%`, background: pct >= 80 ? "#3AB795" : pct >= 50 ? "#FFC107" : "#DD4444" }}></div>
                      </div>
                    </div>
                    <div className="project-btn">
                      <a href={`/donacion?recurso=${encodeURIComponent(n.recurso)}&cantidad=${encodeURIComponent(n.cantidad)}&unidad=${encodeURIComponent(n.unidad)}&centroId=${encodeURIComponent(n.centroId || "")}`} className="btn btn-primary w-100">
                        <i className="bi bi-gift-fill me-1"></i>Donar{falta > 0 ? ` (falta ${falta} ${n.unidad})` : ""}
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ── CÓMO FUNCIONA ── */}
      <div className="mb-5">
        <h2 className="fw-bold mb-1">¿Cómo funciona Donatón?</h2>
        <p className="mb-4 c-muted">
          Un proceso simple, transparente y trazable de principio a fin.
        </p>
        <div className="row g-3">
          {pasos.map((paso, i) => (
            <div key={i} className="col-12 col-md-6 col-lg-3">
              <div className="p-4 rounded-4 h-100 d-flex flex-column gap-2 card-surface">
                <div className="d-flex align-items-center gap-3 mb-1">
                  <span className="numero-paso fw-bold fs-5">{paso.num}</span>
                  <i className={`bi ${paso.icon} fs-4 c-accent`}></i>
                </div>
                <div className="fw-semibold c-heading">{paso.titulo}</div>
                <div className="small c-muted">{paso.texto}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── CTA ── */}
      <div className="cta-section mb-3">
        <h2 className="fw-bold mb-2 c-white">¿Listo para marcar la diferencia?</h2>
        <p className="mb-4 c-pale-red">
          Cada donación, por pequeña que sea, puede cambiarle la vida a una familia en situación de emergencia.
        </p>
        <a href="/donacion" className="btn btn-light btn-lg px-5 btn-light-primary">
          <i className="bi bi-heart-fill me-2"></i>Donar ahora
        </a>
      </div>

    </div>
    </div>
  );
}
