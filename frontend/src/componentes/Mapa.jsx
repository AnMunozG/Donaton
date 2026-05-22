import { APIProvider, Map, Marker, useMap } from '@vis.gl/react-google-maps';

const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '';

function MapController({ center, zoom }) {
  const map = useMap();
  if (map && center) {
    map.panTo(center);
    map.setZoom(zoom || 12);
  }
  return null;
}

export default function Mapa({ centros, seleccionado, onSelect }) {
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
