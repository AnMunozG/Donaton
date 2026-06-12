import { APIProvider, Map, Marker, Polyline, useMap } from '@vis.gl/react-google-maps';
import { useEffect } from 'react';

const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '';

function MapController({ center, zoom }) {
  const map = useMap();
  if (map && center) {
    map.panTo(center);
    map.setZoom(zoom || 12);
  }
  return null;
}

function RoutePolyline({ path }) {
  if (!path || path.length < 2) return null;
  return <Polyline path={path} strokeColor="#dc3545" strokeOpacity={0.85} strokeWeight={5} />;
}

function UserLocationMarker({ position }) {
  if (!position) return null;
  return <Marker position={position} title="Tu ubicación" zIndex={1000} />;
}

function FitBounds({ routeLine }) {
  const map = useMap();

  useEffect(() => {
    if (map && routeLine && routeLine.length > 1 && window.google?.maps?.LatLngBounds) {
      const bounds = new window.google.maps.LatLngBounds();
      routeLine.forEach((p) => bounds.extend(p));
      map.fitBounds(bounds, { padding: 50 });
    }
  }, [map, routeLine]);

  return null;
}

export default function Mapa({ centros, seleccionado, onSelect, routeLine, userLocation }) {
  const center = seleccionado?.coordenadas
    ? { lat: seleccionado.coordenadas.lat, lng: seleccionado.coordenadas.lng }
    : { lat: -33.4489, lng: -70.6693 };

  return (
    <div className="mapa-container">
      <APIProvider apiKey={API_KEY}>
        <Map
          defaultCenter={center}
          defaultZoom={12}
          mapTypeControl={false}
          streetViewControl={false}
          fullscreenControl={false}
          mapId="donaton-map"
          className="mapa-full"
        >
          <MapController center={center} zoom={seleccionado ? 14 : 12} />
          <FitBounds routeLine={routeLine} />
          {centros.map((centro) => (
            centro.coordenadas && (
              <Marker
                key={centro.id}
                position={{ lat: centro.coordenadas.lat, lng: centro.coordenadas.lng }}
                title={centro.nombre}
                onClick={() => onSelect?.(centro)}
              />
            )
          ))}
          <RoutePolyline path={routeLine} />
          <UserLocationMarker position={userLocation} />
        </Map>
      </APIProvider>
      {!API_KEY && (
        <div className="alert alert-warning m-2">
          <small>Configura VITE_GOOGLE_MAPS_API_KEY para ver el mapa</small>
        </div>
      )}
    </div>
  );
}
