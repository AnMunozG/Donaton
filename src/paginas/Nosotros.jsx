import { useState, useEffect } from "react";
import bannerImg from "../assets/Banner.png";
import { getTeam, getValores, getHitos } from "../api.js";

export default function Nosotros() {
  const [team, setTeam] = useState([]);
  const [valores, setValores] = useState([]);
  const [hitos, setHitos] = useState([]);

  useEffect(() => {
    getTeam().then(setTeam);
    getValores().then(setValores);
    getHitos().then(setHitos);
  }, []);

  return (
    <div className="nosotros">

      {/* HERO */}
      <div className="nos-hero" style={{ backgroundImage: `url(${bannerImg})` }}>
        <div className="nos-hero-content">
          <span className="banner-pill mb-3">QUIÉNES SOMOS</span>
          <h1 className="nos-hero-title">Acerca de Donatón</h1>
          <p className="nos-hero-desc">
            Una plataforma abierta que conecta donantes, centros de acopio y comunidades para llevar ayuda humanitaria de forma transparente y eficiente.
          </p>
        </div>
      </div>

      <div className="content-surface">

      {/* IMAGEN + MISIÓN */}
      <div className="row g-4 mb-5 align-items-center">
        <div className="col-lg-5">
          <img src="https://www.agcid.gob.cl/images/08_comu25.png" alt="Nuestra misión en acción" className="nos-image" />
        </div>
        <div className="col-lg-7">
          <h2 className="fw-bold mb-3 c-heading">
            <i className="bi bi-bullseye me-2 c-primary"></i>
            Nuestra misión
          </h2>
          <p className="c-muted nos-paragraph">
            Donatón nació para resolver el caos logístico que ocurre durante emergencias y desastres naturales.
            Nuestra misión es centralizar la gestión de donaciones y necesidades, garantizando que cada recurso
            llegue a quien más lo necesita, en el menor tiempo posible y con total trazabilidad.
          </p>
          <p className="c-muted nos-paragraph">
            Trabajamos con municipalidades, empresas, voluntarios y la sociedad civil para construir
            una red de ayuda que no deje a nadie atrás.
          </p>
        </div>
      </div>

      {/* HISTORIA / HITOS */}
      <div className="mb-5">
        <div className="text-center mb-4">
          <h2 className="fw-bold mb-1 c-heading">Nuestra historia</h2>
          <p className="c-muted">Hitos que han marcado nuestro camino.</p>
        </div>
        <div className="nos-timeline">
          {hitos.map((h, i) => (
            <div key={i} className="nos-milestone">
              <div className="nos-dot">{h.year.slice(-2)}</div>
              <div className="fw-bold c-heading">{h.titulo}</div>
              <div className="small c-muted">{h.texto}</div>
            </div>
          ))}
        </div>
      </div>

      {/* IMAGEN 2 */}
      <div className="mb-5">
        <div className="row g-3">
          <div className="col-md-6">
            <img src="https://www.desarrollosocialyfamilia.gob.cl/storage/image/Enero_2026/23.01_Ayuda.jpg"
              alt="Trabajo en equipo" className="nos-image-16x9" />
          </div>
          <div className="col-md-6">
            <img src="https://global.unitednations.entermediadb.net/assets/mediadb/services/module/asset/downloads/preset/Libraries/Production%20Library/19-11-2024-WFP-Haiti-food-distribution.jpg/image770x420cropped.jpg"
              alt="Distribución de alimentos" className="nos-image-16x9" />
          </div>
        </div>
      </div>

      {/* VALORES */}
      <div className="mb-5">
        <div className="text-center mb-4">
          <h2 className="fw-bold mb-1 c-heading">Nuestros principios</h2>
          <p className="c-muted">Los valores que guían cada decisión.</p>
        </div>
        <div className="row g-3">
          {valores.map((v, i) => (
            <div key={i} className="col-12 col-sm-6 col-lg-3">
              <div className="p-4 rounded-4 h-100 text-center card-surface">
                <div className="value-icon">
                  <i className={`bi ${v.icon}`}></i>
                </div>
                <div className="fw-bold mb-1 c-heading">{v.titulo}</div>
                <div className="small c-muted">{v.texto}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* EQUIPO */}
      <div className="mb-2">
        <div className="text-center mb-4">
          <h2 className="fw-bold mb-1 c-heading">Equipo de desarrollo</h2>
          <p className="c-muted">Los creadores detrás de Donatón.</p>
        </div>
        <div className="row g-3 justify-content-center">
          {team.map((p, i) => (
            <div key={i} className="col-12 col-md-4">
              <div className="p-4 rounded-4 text-center h-100 card-surface">
                <div className="team-avatar" style={{ background: p.color }}>
                  {p.nombre.split(" ").map((n) => n[0]).slice(0, 2).join("")}
                </div>
                <div className="fw-bold c-heading">{p.nombre}</div>
                <div className="small c-muted">{p.rol}</div>
                <div className="team-divider" style={{ background: p.color }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
    </div>
  );
}
