import { useState, useRef, useEffect } from "react";

const REGIONES = [
  "Arica y Parinacota",
  "Tarapacá",
  "Antofagasta",
  "Atacama",
  "Coquimbo",
  "Valparaíso",
  "Metropolitana de Santiago",
  "O'Higgins",
  "Maule",
  "Ñuble",
  "Biobío",
  "La Araucanía",
  "Los Ríos",
  "Los Lagos",
  "Aysén del General Carlos Ibáñez del Campo",
  "Magallanes y de la Antártica Chilena",
];

export default function SelectRegion({ value, onChange, error }) {
  const [abierto, setAbierto] = useState(false);
  const [filtro, setFiltro] = useState("");
  const wrapperRef = useRef(null);

  const filtradas = REGIONES.filter((r) =>
    r.toLowerCase().includes(filtro.toLowerCase())
  );

  useEffect(() => {
    function handler(e) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target)) {
        setAbierto(false);
        setFiltro("");
      }
    }
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  function seleccionar(region) {
    onChange({ target: { name: "region", value: region } });
    setAbierto(false);
    setFiltro("");
  }

  return (
    <div className="position-relative" ref={wrapperRef}>
      <label className="form-label small fw-semibold">Región</label>
      <input
        name="region"
        className={`form-control${error ? " is-invalid" : ""}`}
        value={abierto ? filtro : value || ""}
        onFocus={() => { setAbierto(true); setFiltro(value || ""); }}
        onChange={(e) => {
          setFiltro(e.target.value);
          setAbierto(true);
          if (!abierto) return;
        }}
        placeholder="Escribe para buscar una región..."
        autoComplete="off"
      />
      {error && <div className="invalid-feedback d-block">{error}</div>}
      {abierto && (
        <ul
          className="list-group position-absolute w-100 shadow-sm"
          style={{ zIndex: 1050, maxHeight: 240, overflowY: "auto" }}
        >
          {filtradas.length === 0 ? (
            <li className="list-group-item text-muted small">Sin resultados</li>
          ) : (
            filtradas.map((r) => (
              <li
                key={r}
                className={`list-group-item list-group-item-action small cursor-pointer ${
                  r === value ? "active" : ""
                }`}
                onClick={() => seleccionar(r)}
                style={{ cursor: "pointer" }}
              >
                {r}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
