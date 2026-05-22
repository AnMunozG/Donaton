import { Link } from "react-router-dom";
import { DonatonLogo } from "./Logos.jsx";

export default function Footer() {
  return (
    <footer>
      <div className="container-fluid">
        <div className="row">
          <div className="col-12 col-md-4 mb-4 mb-md-0">
            <Link to="/" className="d-flex align-items-center mb-3 link-body-emphasis text-decoration-none">
              <DonatonLogo variante="pequeño" />
            </Link>
            <p className="footer-text">
              Conectando corazones para apoyar a quienes más lo necesitan. Tu aporte hace la diferencia en nuestra comunidad.
            </p>
          </div>

          <div className="col-6 col-md-2 mb-3">
            <h5>Navegación</h5>
            <ul className="nav flex-column">
              <li className="nav-item mb-2"><Link to="/" className="nav-link p-0">Inicio</Link></li>
              <li className="nav-item mb-2"><Link to="/nosotros" className="nav-link p-0">Acerca de nosotros</Link></li>
              <li className="nav-item mb-2"><Link to="/centros" className="nav-link p-0">Nuestros centros</Link></li>
              <li className="nav-item mb-2"><Link to="/necesidades" className="nav-link p-0">Necesidades</Link></li>
            </ul>
          </div>

          <div className="col-6 col-md-3 mb-3">
            <h5>Contacto</h5>
            <ul className="nav flex-column">
              <li className="footer-contact-item"><i className="bi bi-geo-alt-fill me-2 c-accent"></i>Antonio Varas 666, Providencia, Región Metropolitana</li>
              <li className="footer-contact-item"><i className="bi bi-telephone-fill me-2 c-accent"></i>+56 9 1234 5678</li>
              <li className="footer-contact-item"><i className="bi bi-envelope-fill me-2 c-accent"></i>contacto@donaton.cl</li>
            </ul>
          </div>

          <div className="col-md-3">
            <h5>Síguenos</h5>
            <div className="d-flex gap-3 fs-4">
              <a href="#" className="footer-social-link"><i className="bi bi-facebook"></i></a>
              <a href="#" className="footer-social-link"><i className="bi bi-instagram"></i></a>
              <a href="#" className="footer-social-link"><i className="bi bi-twitter-x"></i></a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="footer-text">
            &copy; 2026 <a href="https://www.duoc.cl" target="_blank" rel="noopener noreferrer">Duoc UC</a>, Org. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
}
