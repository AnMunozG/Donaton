import { useState, useEffect, useRef } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { DonatonLogo } from "./Logos.jsx";
import { useAuth } from "./AuthContext";

export default function Header() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const { user, isAuth, logout } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    setMenuOpen(false);
    setDropdownOpen(false);
  }, [pathname]);

  useEffect(() => {
    const handleClick = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header>
      <nav className="navbar navbar-expand-md w-100">
        <Link to="/" className="navbar-brand logo-link">
          <DonatonLogo variante="pequeño" />
        </Link>

        <button
          className="navbar-toggler"
          type="button"
          aria-controls="navbarContent"
          aria-expanded={menuOpen}
          aria-label="Toggle navigation"
          onClick={() => setMenuOpen((prev) => !prev)}
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className={`collapse navbar-collapse${menuOpen ? " show" : ""}`} id="navbarContent">
          <ul className="navbar-nav me-auto mb-2 mb-md-0">
            <li className="nav-item">
              <Link to="/" className={`nav-link${pathname === "/" ? " active" : ""}`}>
                Inicio
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/nosotros" className={`nav-link${pathname === "/nosotros" ? " active" : ""}`}>
                Acerca de Nosotros
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/centros" className={`nav-link${pathname === "/centros" ? " active" : ""}`}>
                Nuestros Centros
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/necesidades" className={`nav-link${pathname === "/necesidades" ? " active" : ""}`}>
                Necesidades
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/transparencia" className={`nav-link${pathname === "/transparencia" ? " active" : ""}`}>
                Transparencia
              </Link>
            </li>
          </ul>

          <div className="header-actions">
            <Link to="/donacion" className="btn btn-outline-accent">
              <i className="bi bi-heart-fill me-1"></i>Donar
            </Link>
            {!isAuth ? (
              <>
                <Link to="/registro" className="btn btn-primary">
                  Hacerse socio
                </Link>
                <Link to="/login" className="btn btn-outline-secondary">
                  Iniciar sesión
                </Link>
              </>
            ) : (
              <div className="dropdown" ref={dropdownRef}>
                <button
                  className="btn btn-accent dropdown-toggle d-flex align-items-center gap-2 user-dropdown-btn"
                  onClick={() => setDropdownOpen((prev) => !prev)}
                >
                  <i className="bi bi-person-circle"></i>
                  <span className="d-none d-md-inline">{user.nombre || "Usuario"}</span>
                </button>
                {dropdownOpen && (
                  <ul className="dropdown-menu dropdown-menu-end show user-dropdown-menu">
                    {user.rol === "admin" && (
                      <li>
                        <Link to="/dashboard" className="dropdown-item" onClick={() => setDropdownOpen(false)}>
                          <i className="bi bi-speedometer2 me-2"></i>Dashboard
                        </Link>
                      </li>
                    )}
                    <li>
                      <Link to="/perfil" className="dropdown-item" onClick={() => setDropdownOpen(false)}>
                        <i className="bi bi-person-fill me-2"></i>Perfil
                      </Link>
                    </li>
                    <li><hr className="dropdown-divider" /></li>
                    <li>
                      <button className="dropdown-item" onClick={handleLogout}>
                        <i className="bi bi-box-arrow-right me-2"></i>Cerrar sesión
                      </button>
                    </li>
                  </ul>
                )}
              </div>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
}
