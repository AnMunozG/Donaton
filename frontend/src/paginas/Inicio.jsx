import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { DonatonLogo } from "../componentes/Logos.jsx";
import { getCategoriasDonacion, getPasosFuncionamiento, getNecesidades, getCentros, contarVoluntariosAsignados } from "../api.js";
import { formatearNumero } from "../componentes/Validaciones.js";
import bannerInicioImg from "../assets/BannerInicio.png";
import inicioImg1 from "../assets/Inicio (1).jpg";
import inicioImg2 from "../assets/Inicio (2).jpg";


function ProyectoCard({ n, centroNombre, voluntarioCounts }) {
  const total = Number(n.cantidad);
  const donado = Number(n.donado) || 0;
  const pct = total > 0 ? Math.round((donado / total) * 100) : 0;
  const falta = total - donado;
  const fecha = n.fecha ? new Date(n.fecha).toLocaleDateString("es-CL", { year: "numeric", month: "long", day: "numeric" }) : "";
  const d = n.detalles || {};
  const esVoluntariado = n.categoria === "VOLUNTARIADO";
  const voluntariosInscritos = voluntarioCounts[n.id] || 0;
  const voluntariosReq = d.numVoluntarios || (esVoluntariado ? total : 0);

  return (
    <div className="col-12 col-md-6 col-lg-4">
      <div className="project-card">
        <div className="d-flex align-items-start justify-content-between mb-2">
          <span className={`badge bg-${n.urgencia === "Alta" ? "danger" : n.urgencia === "Media" ? "warning" : "success"}`}>
            <i className="bi bi-exclamation-triangle-fill me-1"></i>{n.urgencia}
          </span>
          <span className="project-id">#{n.id}</span>
        </div>

        <h3 className="project-resource">{n.recurso}</h3>

        <div className="d-flex gap-3 small c-muted mb-2">
          <span>
            <i className="bi bi-building me-1 c-accent"></i>{centroNombre(n.centroId) || n.centro || "Sin centro"}
          </span>
          {fecha && (
            <span>
              <i className="bi bi-calendar3 me-1 c-accent"></i>{fecha}
            </span>
          )}
        </div>

        {n.descripcion && (
          <div className="project-desc small mb-2" dangerouslySetInnerHTML={{ __html: n.descripcion }} />
        )}

        {esVoluntariado ? (
          <div className="small mb-2 d-flex flex-column gap-1">
            {d.actividad && (
              <span className="c-muted"><i className="bi bi-tools me-1 c-primary"></i><strong>Actividad:</strong> {d.actividad}</span>
            )}
            {(d.horaDesde || d.horaHasta) && (
              <span className="c-muted"><i className="bi bi-clock me-1 c-primary"></i><strong>Horario:</strong> {d.horaDesde || "?"} - {d.horaHasta || "?"}</span>
            )}
            {d.dias && (
              <span className="c-muted"><i className="bi bi-calendar-week me-1 c-primary"></i><strong>Días:</strong> {Array.isArray(d.dias) ? d.dias.join(", ") : d.dias}</span>
            )}
            {d.numVoluntarios && (
              <span className="c-muted"><i className="bi bi-people-fill me-1 c-primary"></i><strong>Voluntarios necesarios:</strong> {d.numVoluntarios}</span>
            )}
            {(d.contactoEmail || d.contactoTel) && (
              <span className="c-muted"><i className="bi bi-envelope me-1 c-primary"></i><strong>Contacto:</strong> {d.contactoEmail || ""}{d.contactoEmail && d.contactoTel ? " | " : ""}{d.contactoTel || ""}</span>
            )}
          </div>
        ) : (
          d.contactoEmail || d.contactoTel || d.fechaLimite ? (
            <div className="small mb-2 d-flex flex-column gap-1">
              {d.contactoEmail && (
                <span className="c-muted"><i className="bi bi-envelope me-1 c-primary"></i><strong>Contacto:</strong> {d.contactoEmail}</span>
              )}
              {d.contactoTel && !d.contactoEmail && (
                <span className="c-muted"><i className="bi bi-telephone me-1 c-primary"></i><strong>Contacto:</strong> {d.contactoTel}</span>
              )}
              {d.fechaLimite && (
                <span className="c-muted"><i className="bi bi-calendar-exclamation me-1 c-primary"></i><strong>Fecha límite:</strong> {new Date(d.fechaLimite).toLocaleDateString("es-CL")}</span>
              )}
            </div>
          ) : null
        )}

        {esVoluntariado ? (
          <div className="mb-2">
            <div className="d-flex justify-content-between small mb-1">
              <span className="c-muted"><strong className="c-heading">Voluntarios:</strong> {voluntariosInscritos} / {voluntariosReq} inscritos</span>
              <span className="fw-semibold" style={{ color: voluntariosInscritos >= voluntariosReq ? "#3AB795" : "#DD4444" }}>
                {voluntariosReq > 0 ? Math.round((voluntariosInscritos / voluntariosReq) * 100) : 0}%
              </span>
            </div>
            <div className="progress progress-height-6">
              <div className="progress-bar progress-bar-rounded" style={{ width: `${voluntariosReq > 0 ? Math.round((voluntariosInscritos / voluntariosReq) * 100) : 0}%`, backgroundColor: voluntariosInscritos >= voluntariosReq ? "#3AB795" : "#DD4444" }}></div>
            </div>
          </div>
        ) : (
          <div className="mb-2">
            <div className="d-flex justify-content-between small mb-1">
              <span className="c-muted"><strong className="c-heading">Recaudado:</strong> {formatearNumero(donado)} / {formatearNumero(total)} {n.unidad}</span>
              <span className="fw-semibold color-dynamic" style={{ '--dynamic-color': pct >= 80 ? "#3AB795" : pct >= 50 ? "#FFC107" : "#DD4444" }}>{pct}%</span>
            </div>
            <div className="progress progress-height-6">
              <div className="progress-bar progress-bar-rounded progress-dynamic-bar" style={{ '--bar-w': `${pct}%`, '--bar-color': pct >= 80 ? "#3AB795" : pct >= 50 ? "#FFC107" : "#DD4444" }}></div>
            </div>
          </div>
        )}

        <div className="project-btn">
          {esVoluntariado ? (
            <Link to="/voluntarios" className="btn btn-accent w-100">
              <i className="bi bi-people-fill me-1"></i>Registrarme como voluntario
            </Link>
          ) : (
            <Link to={`/donacion?recurso=${encodeURIComponent(n.recurso)}&cantidad=${encodeURIComponent(n.cantidad)}&unidad=${encodeURIComponent(n.unidad)}&centroId=${encodeURIComponent(n.centroId || "")}`} className="btn btn-primary w-100">
              <i className="bi bi-gift-fill me-1"></i>Donar{falta > 0 ? ` (falta ${formatearNumero(falta)} ${n.unidad})` : ""}
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}


export default function Inicio() {
  const [categorias, setCategorias] = useState([]);
  const [pasos, setPasos] = useState([]);
  const [necesidades, setNecesidades] = useState([]);
  const [centros, setCentros] = useState([]);
  const [voluntarioCounts, setVoluntarioCounts] = useState({});

  useEffect(() => {
    getCategoriasDonacion().then(setCategorias);
    getPasosFuncionamiento().then(setPasos);
    getCentros().then(setCentros);
  }, []);

  useEffect(() => {
    getNecesidades().then(async (todas) => {
      setNecesidades(todas);
      const volunteerNeeds = (Array.isArray(todas) ? todas : []).filter(
        (n) => n.categoria === "VOLUNTARIADO" && n.estado !== "Cubierta" && n.estado !== "Pendiente"
      );
      const counts = {};
      for (const op of volunteerNeeds) {
        try { counts[op.id] = await contarVoluntariosAsignados(op.id); } catch { counts[op.id] = 0; }
      }
      setVoluntarioCounts(counts);
    });
  }, []);

  const centroNombre = (centroId) => centros.find((c) => c.id === centroId)?.nombre || "";

  const items = [...categorias, ...categorias];
  const urgenciaPeso = { Alta: 0, Media: 1, Baja: 2 };
  const activas = necesidades
    .filter((n) => n.estado !== "Cubierta" && n.estado !== "Pendiente")
    .sort((a, b) => {
      const ua = urgenciaPeso[a.urgencia] ?? 99;
      const ub = urgenciaPeso[b.urgencia] ?? 99;
      if (ua !== ub) return ua - ub;
      const pctA = Number(a.cantidad) > 0 ? Number(a.donado) / Number(a.cantidad) : 0;
      const pctB = Number(b.cantidad) > 0 ? Number(b.donado) / Number(b.cantidad) : 0;
      return pctB - pctA;
    })
    .slice(0, 6);

  return (
    <div className="inicio">

      <div className="hero-banner hero-banner-pagina" style={{ backgroundImage: `url(${bannerInicioImg})` }}>
        <div className="hero-banner-content">
          <DonatonLogo variante="banner" />
          <h2>Coordinando la ayuda donde más se necesita</h2>
          <p>
            Donatón conecta a donantes, empresas, municipalidades y equipos logísticos
            para llevar ayuda humanitaria de forma transparente y eficiente a quienes más lo necesitan.
          </p>
          <div className="d-flex gap-3 justify-content-center mt-4 flex-wrap">
            <Link to="/donacion" className="btn btn-primary btn-lg px-4">
              <i className="bi bi-heart-fill me-2"></i>Hacer una donación
            </Link>
            <Link to="/necesidades" className="btn btn-accent btn-lg px-4">
              <i className="bi bi-flag-fill me-2"></i>Reportar una necesidad
            </Link>
          </div>
        </div>
      </div>

      <div className="content-surface">

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
            <Link to="/transparencia" className="btn btn-accent btn-lg px-4">
              <i className="bi bi-info-circle-fill me-2"></i>Saber más
            </Link>
          </div>
        </div>
      </div>

      <div className="row g-4 mb-5 align-items-center">
        <div className="col-md-5">
          <div className="img-placeholder rounded-4"
            style={{ backgroundImage: `url("${inicioImg1}")` }}></div>
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
                  <i className={`bi ${cat.icono} fs-2 mb-3 d-block c-accent`}></i>
                  <div className="fw-semibold mb-1 c-heading">{cat.nombre}</div>
                  <div className="small c-muted">{cat.descripcion}</div>
                </div>
              ))}
            </div>
          </div>
          <Link to="/donacion" className="btn btn-success btn-lg px-4 mt-3 d-block mx-auto btn-fit">
            <i className="bi bi-heart-fill me-1"></i>Ir a donar
          </Link>
        </div>
        <div className="col-md-5">
          <div className="img-placeholder rounded-4"
            style={{ backgroundImage: `url("${inicioImg2}")` }}></div>
        </div>
      </div>

      <div className="mb-5">
        <h2 className="fw-bold mb-1">Proyectos activos</h2>
        <p className="mb-4 c-muted">Necesidades reportadas en terreno que requieren tu ayuda.</p>
        {activas.length > 0 ? (
          <div className="row g-3">
            {activas.map((n) => (
              <ProyectoCard key={n.id} n={n} centroNombre={centroNombre} voluntarioCounts={voluntarioCounts} />
            ))}
          </div>
        ) : (
          <div className="text-center py-5">
            <i className="bi bi-inbox fs-1 c-muted d-block mb-2"></i>
            <p className="c-muted mb-0">Ningún proyecto visible ahora mismo...</p>
          </div>
        )}
      </div>

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
                  <span className="numero-paso fw-bold fs-5">{paso.paso}</span>
                  <i className={`bi ${paso.icono} fs-4 c-accent`}></i>
                </div>
                <div className="fw-semibold c-heading">{paso.titulo}</div>
                <div className="small c-muted">{paso.descripcion}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="cta-section mb-3">
        <h2 className="fw-bold mb-2 c-white">¿Listo para marcar la diferencia?</h2>
        <p className="mb-4 c-pale-red">
          Cada donación, por pequeña que sea, puede cambiarle la vida a una familia en situación de emergencia.
        </p>
        <Link to="/donacion" className="btn btn-light btn-lg px-5 btn-light-primary">
          <i className="bi bi-heart-fill me-2"></i>Donar ahora
        </Link>
      </div>

    </div>
    </div>
  );
}
