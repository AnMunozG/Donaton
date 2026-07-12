import { useState, useRef, useEffect } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const iconMarker = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  shadowSize: [41, 41],
});

export default function AddressPicker({ onLocationChange, initialLocation, label = "Dirección" }) {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(initialLocation || null);
  const [error, setError] = useState("");
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const markerRef = useRef(null);
  const debounceRef = useRef(null);

  useEffect(() => {
    if (!mapRef.current || mapInstance.current) return;

    const center = initialLocation
      ? [initialLocation.lat, initialLocation.lng]
      : [-33.4489, -70.6693];

    const map = L.map(mapRef.current, {
      center,
      zoom: 13,
      zoomControl: true,
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; OSM',
      maxZoom: 19,
    }).addTo(map);

    map.on("click", (e) => {
      const { lat, lng } = e.latlng;
      placeMarker(lat, lng);
      reverseGeocode(lat, lng);
    });

    mapInstance.current = map;

    if (initialLocation) {
      placeMarker(initialLocation.lat, initialLocation.lng);
    }

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  function placeMarker(lat, lng) {
    const map = mapInstance.current;
    if (!map) return;

    if (markerRef.current) map.removeLayer(markerRef.current);

    markerRef.current = L.marker([lat, lng], { icon: iconMarker, draggable: true })
      .addTo(map)
      .on("dragend", () => {
        const pos = markerRef.current.getLatLng();
        handleLocation(pos.lat, pos.lng);
      });

    map.setView([lat, lng], 15);
    handleLocation(lat, lng);
  }

  function handleLocation(lat, lng) {
    setSelected({ lat, lng });
    if (onLocationChange) onLocationChange({ lat, lng });
    setError("");
  }

  async function reverseGeocode(lat, lng) {
    try {
      const res = await fetch(
        `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&addressdetails=1&accept-language=es`,
        { headers: { "User-Agent": "Donaton/1.0" } }
      );
      const data = await res.json();
      if (data.display_name) {
        setQuery(data.display_name);
      }
    } catch {
      // silently fail
    }
  }

  function handleQueryChange(value) {
    setQuery(value);
    setError("");

    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (value.length < 3) {
      setSuggestions([]);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(
          `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(value)}&format=json&limit=5&addressdetails=1&accept-language=es`,
          { headers: { "User-Agent": "Donaton/1.0" } }
        );
        const data = await res.json();
        setSuggestions(data);
      } catch {
        setSuggestions([]);
      } finally {
        setLoading(false);
      }
    }, 400);
  }

  function selectSuggestion(item) {
    setSuggestions([]);
    setQuery(item.display_name);
    const lat = parseFloat(item.lat);
    const lng = parseFloat(item.lon);
    placeMarker(lat, lng);
  }

  return (
    <div className="address-picker">
      <label className="form-label small fw-semibold">{label}</label>
      <div className="position-relative">
        <input
          type="text"
          className={`form-control ${error ? "is-invalid" : ""}`}
          placeholder="Busca una dirección..."
          value={query}
          onChange={(e) => handleQueryChange(e.target.value)}
        />
        {loading && (
          <div className="position-absolute end-0 top-0 mt-2 me-3">
            <span className="spinner-border spinner-border-sm" role="status"></span>
          </div>
        )}
        {suggestions.length > 0 && (
          <ul className="list-group position-absolute w-100 shadow-sm dropdown-scrollable" style={{ maxHeight: 200 }}>
            {suggestions.map((item, i) => (
              <li
                key={i}
                className="list-group-item list-group-item-action py-2 small cursor-pointer"
                onClick={() => selectSuggestion(item)}
              >
                <i className="bi bi-geo-alt me-1 c-accent"></i>
                {item.display_name}
              </li>
            ))}
          </ul>
        )}
      </div>
      {error && <div className="invalid-feedback d-block">{error}</div>}
      <div ref={mapRef} className="map-sm mt-2 rounded-3 border"></div>
      {selected && (
        <div className="small c-muted mt-1">
          <i className="bi bi-crosshair me-1"></i>
          {selected.lat.toFixed(5)}, {selected.lng.toFixed(5)}
        </div>
      )}
    </div>
  );
}
