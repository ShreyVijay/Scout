// frontend/src/components/map/MapView.jsx
import { createContext, useState, useEffect, useRef, useCallback, useMemo } from 'react';

export const MapContext = createContext(null);

const HOST_CITIES_COORDS = {
  "Seattle": { x: 18, y: 15, lat: 47.6062, lng: -122.3321 },
  "Vancouver": { x: 14, y: 10, lat: 49.2827, lng: -123.1207 },
  "San Francisco": { x: 10, y: 36, lat: 37.7749, lng: -122.4194 },
  "Los Angeles": { x: 13, y: 48, lat: 34.0522, lng: -118.2437 },
  "Guadalajara": { x: 30, y: 82, lat: 20.6597, lng: -103.3496 },
  "Mexico City": { x: 35, y: 88, lat: 19.4326, lng: -99.1332 },
  "Monterrey": { x: 36, y: 74, lat: 25.6866, lng: -100.3161 },
  "Kansas City": { x: 48, y: 42, lat: 39.0997, lng: -94.5786 },
  "Dallas": { x: 48, y: 62, lat: 32.7767, lng: -96.7970 },
  "Houston": { x: 50, y: 70, lat: 29.7604, lng: -95.3698 },
  "Atlanta": { x: 68, y: 58, lat: 33.7490, lng: -84.3880 },
  "Miami": { x: 78, y: 78, lat: 25.7617, lng: -80.1918 },
  "New York": { x: 84, y: 31, lat: 40.7128, lng: -74.0060 },
  "Philadelphia": { x: 82, y: 35, lat: 39.9526, lng: -75.1652 },
  "Boston": { x: 86, y: 25, lat: 42.3601, lng: -71.0589 },
  "New York/New Jersey": { x: 84, y: 31, lat: 40.7128, lng: -74.0060 },
  "Toronto": { x: 74, y: 24, lat: 43.6532, lng: -79.3832 }
};

export default function MapView({ children, centerCity = "Miami", height = "400px" }) {
  const [googleMapsLoaded, setGoogleMapsLoaded] = useState(false);
  const [mapInstance, setMapInstance] = useState(null);
  const mapRef = useRef(null);

  // Fallback map state
  const [activeMarkers, setActiveMarkers] = useState([]);
  const [activePaths, setActivePaths] = useState([]);
  const [selectedElement, setSelectedElement] = useState(null);

  // Registration helpers for children components (mock or real)
  const registerMarker = useCallback((marker) => {
    setActiveMarkers(prev => {
      if (prev.find(m => m.id === marker.id)) return prev;
      return [...prev, marker];
    });
  }, []);

  const unregisterMarker = useCallback((id) => {
    setActiveMarkers(prev => prev.some(m => m.id === id) ? prev.filter(m => m.id !== id) : prev);
  }, []);

  const registerPath = useCallback((path) => {
    setActivePaths(prev => {
      if (prev.find(p => p.id === path.id)) return prev;
      return [...prev, path];
    });
  }, []);

  const unregisterPath = useCallback((id) => {
    setActivePaths(prev => prev.some(p => p.id === id) ? prev.filter(p => p.id !== id) : prev);
  }, []);

  useEffect(() => {
    const key = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
    if (window.google?.maps) {
      setGoogleMapsLoaded(true);
      return;
    }

    if (!key) {
      // No key, directly use fallback
      return;
    }

    // Load google maps script
    const scriptId = 'google-maps-script';
    if (!document.getElementById(scriptId)) {
      const script = document.createElement('script');
      script.id = scriptId;
      script.src = `https://maps.googleapis.com/maps/api/js?key=${key}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = () => setGoogleMapsLoaded(true);
      document.head.appendChild(script);
    }
  }, []);

  // Initialize Real Google Map if script loaded
  useEffect(() => {
    if (googleMapsLoaded && mapRef.current && !mapInstance) {
      const centerCoord = HOST_CITIES_COORDS[centerCity] || HOST_CITIES_COORDS["Miami"];
      const gMap = new window.google.maps.Map(mapRef.current, {
        center: { lat: centerCoord.lat, lng: centerCoord.lng },
        zoom: 4,
        styles: [
          {
            elementType: 'geometry',
            stylers: [{ color: '#1a1a2e' }]
          },
          {
            elementType: 'labels.text.stroke',
            stylers: [{ color: '#1a1a2e' }]
          },
          {
            elementType: 'labels.text.fill',
            stylers: [{ color: '#8ec3b9' }]
          }
        ]
      });
      setMapInstance(gMap);
    }
  }, [googleMapsLoaded, centerCity, mapInstance]);

  // Context value for children
  const contextValue = useMemo(() => ({
    googleMapsLoaded,
    mapInstance,
    centerCoords: HOST_CITIES_COORDS[centerCity] || HOST_CITIES_COORDS["Miami"],
    cityCoordsMap: HOST_CITIES_COORDS,
    registerMarker,
    unregisterMarker,
    registerPath,
    unregisterPath
  }), [googleMapsLoaded, mapInstance, centerCity, registerMarker, unregisterMarker, registerPath, unregisterPath]);

  // Helper to resolve coordinates on SVG
  const getSvgCoordinates = (marker) => {
    if (marker.city && HOST_CITIES_COORDS[marker.city]) {
      const cityCoords = HOST_CITIES_COORDS[marker.city];
      // Jitter slightly based on marker id/type to avoid perfect overlap
      const seed = marker.id ? marker.id.charCodeAt(0) + (marker.id.charCodeAt(1) || 0) : 0;
      const jitterX = marker.type !== 'city' ? ((seed % 7) - 3) * 0.8 : 0;
      const jitterY = marker.type !== 'city' ? (((seed >> 1) % 7) - 3) * 0.8 : 0;
      return { x: cityCoords.x + jitterX, y: cityCoords.y + jitterY };
    }
    // Default fallback
    return { x: 50, y: 50 };
  };

  return (
    <MapContext.Provider value={contextValue}>
      <div id="scout-map-wrapper" style={{ position: 'relative', width: '100%', marginBottom: '1.5rem' }}>
        <div style={{ display: 'none' }}>{children}</div>
        {googleMapsLoaded ? (
          <div ref={mapRef} style={{ width: '100%', minHeight: height === '100%' ? '420px' : undefined, height, borderRadius: '8px', border: '1px solid var(--c-border)' }} />
        ) : (
          /* Premium Custom SVG Fallback Map */
          <div
            className="fallback-map-container"
            style={{
              width: '100%',
              height,
              backgroundColor: '#111122',
              position: 'relative',
              borderRadius: '8px',
              border: '1px solid #333355',
              overflow: 'hidden',
              userSelect: 'none'
            }}
          >
            {/* Dark grid background */}
            <svg
              width="100%"
              height="100%"
              viewBox="0 0 100 100"
              preserveAspectRatio="none"
              style={{ position: 'absolute', top: 0, left: 0 }}
            >
              <defs>
                <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#22223c" strokeWidth="0.5" />
                </pattern>
              </defs>
              <rect width="100%" height="100%" fill="url(#grid)" />

              {/* Geographic North America borders draft */}
              <path
                d="M 5,20 Q 20,5 50,15 T 95,25 Q 98,40 90,60 T 75,95 Q 60,95 40,88 T 10,65 Z"
                fill="none"
                stroke="#1b1b36"
                strokeWidth="1.5"
                strokeDasharray="4 4"
              />

              {/* Inactive host cities back-dots */}
              {Object.entries(HOST_CITIES_COORDS).map(([name, coords]) => (
                <g key={name}>
                  <circle cx={coords.x} cy={coords.y} r="0.75" fill="#333355" />
                  <text
                    x={coords.x}
                    y={coords.y - 1.5}
                    fill="#444466"
                    fontSize="9px"
                    textAnchor="middle"
                  >
                    {name}
                  </text>
                </g>
              ))}

              {/* Active Route/Itinerary Connections */}
              {activePaths.map((path) => {
                if (!path.stops) return null;
                const coordinates = path.stops.map(stopName => HOST_CITIES_COORDS[stopName]).filter(Boolean);
                if (coordinates.length < 2) return null;
                
                const d = coordinates.map((c, i) => `${i === 0 ? 'M' : 'L'} ${c.x} ${c.y}`).join(' ');
                
                return (
                  <path
                    key={path.id}
                    d={d}
                    fill="none"
                    stroke={path.color || '#2d6a4f'}
                    strokeWidth="3.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    opacity="0.85"
                  />
                );
              })}

              {/* Specific Directions route (origin -> destination) */}
              {activePaths.map((path) => {
                if (path.type === 'directions') {
                  const start = HOST_CITIES_COORDS[path.startCity];
                  const end = HOST_CITIES_COORDS[path.endCity];
                  if (!start || !end) return null;
                  
                  return (
                    <path
                      key={`dir-${path.id}`}
                      d={`M ${start.x} ${start.y} Q ${(start.x + end.x) / 2} ${Math.min(start.y, end.y) - 10} ${end.x} ${end.y}`}
                      fill="none"
                      stroke="#e67e22"
                      strokeWidth="3"
                      strokeLinecap="round"
                      strokeDasharray="5 3"
                    />
                  );
                }
                return null;
              })}
            </svg>

            {/* Interactive Markers */}
            {activeMarkers.map((marker) => {
              const pos = getSvgCoordinates(marker);
              const isSelected = selectedElement && selectedElement.id === marker.id;
              
              let color = '#2d6a4f'; // Itinerary
              let symbol = '⚽';
              if (marker.type === 'hotel') {
                color = '#0d6efd';
                symbol = '🏨';
              } else if (marker.type === 'food') {
                color = '#dc3545';
                symbol = '🍔';
              } else if (marker.type === 'recommended') {
                color = '#e67e22';
                symbol = '⭐';
              }

              const getCode = (t) => {
                const m = {
                  'Argentina': 'ar', 'Brazil': 'br', 'USA': 'us', 'Mexico': 'mx', 'Canada': 'ca',
                  'England': 'gb-eng', 'France': 'fr', 'Germany': 'de', 'Spain': 'es', 'Portugal': 'pt',
                  'Japan': 'jp', 'South Korea': 'kr', 'Egypt': 'eg', 'Morocco': 'ma', 'Senegal': 'sn',
                  'Colombia': 'co', 'Uruguay': 'uy', 'Croatia': 'hr', 'Netherlands': 'nl', 'Belgium': 'be'
                };
                return m[t] || 'un';
              };

              let content = <div style={{ fontSize: '13px' }}>{symbol}</div>;
              if (marker.type === 'city' && marker.team) {
                content = (
                  <img 
                    src={`https://flagcdn.com/w20/${getCode(marker.team)}.png`}
                    alt={marker.team}
                    style={{ width: '16px', borderRadius: '2px', objectFit: 'cover' }}
                    onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'block'; }}
                  />
                );
              }

              return (
                <div
                  key={marker.id}
                  style={{
                    position: 'absolute',
                    left: `${pos.x}%`,
                    top: `${pos.y}%`,
                    transform: 'translate(-50%, -50%)',
                    cursor: 'pointer',
                    zIndex: isSelected ? 20 : 10
                  }}
                  onClick={() => setSelectedElement(marker)}
                >
                  <div
                    style={{
                      width: '28px',
                      height: '28px',
                      borderRadius: '50%',
                      backgroundColor: color,
                      border: '2px solid white',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: '0 2px 5px rgba(0,0,0,0.5)',
                      transition: 'transform 0.15s ease'
                    }}
                    onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.25)'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)'; }}
                  >
                    {content}
                    {marker.type === 'city' && marker.team && <div style={{ display: 'none', fontSize: '13px' }}>⚽</div>}
                  </div>
                </div>
              );
            })}

            {/* Popover overlay for details */}
            {selectedElement && (
              <div
                className="card"
                style={{
                  position: 'absolute',
                  bottom: '10px',
                  left: '10px',
                  width: 'calc(100% - 20px)',
                  backgroundColor: 'var(--c-surface)',
                  color: 'var(--c-t1)',
                  padding: '16px',
                  zIndex: 30,
                  boxShadow: '0 8px 24px rgba(0,0,0,0.5)',
                  border: '1px solid var(--c-border)',
                  borderRadius: '12px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <h4 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 'bold' }}>
                      {selectedElement.name || selectedElement.title}
                    </h4>
                    {selectedElement.type === 'city' && (
                      <span style={{ fontSize: '0.85rem', color: 'var(--c-amber)', fontWeight: 'bold' }}>
                        {selectedElement.stadium}
                      </span>
                    )}
                  </div>
                  <button
                    style={{ background: 'var(--c-background)', border: '1px solid var(--c-border)', borderRadius: '50%', width: '28px', height: '28px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--c-t1)' }}
                    onClick={() => setSelectedElement(null)}
                  >
                    ✕
                  </button>
                </div>
                
                <div style={{ fontSize: '0.9rem', color: 'var(--c-t2)', display: 'grid', gap: '4px' }}>
                  {selectedElement.type === 'hotel' && (
                    <>
                      <div><strong>Rating:</strong> ⭐ {selectedElement.rating}</div>
                      <div><strong>Price:</strong> {'$'.repeat(selectedElement.price_level)}</div>
                      <div><strong>Distance:</strong> {selectedElement.distance}</div>
                      <div style={{ marginTop: '4px' }}>{selectedElement.address}</div>
                    </>
                  )}
                  {selectedElement.type === 'food' && (
                    <>
                      <div><strong>Rating:</strong> ⭐ {selectedElement.rating}</div>
                      <div><strong>Category:</strong> {selectedElement.category}</div>
                      <div><strong>Price:</strong> {'$'.repeat(selectedElement.price_level)}</div>
                      <div style={{ marginTop: '4px' }}>{selectedElement.address}</div>
                    </>
                  )}
                  {selectedElement.type === 'city' && (
                    <>
                      <div><strong>City:</strong> {selectedElement.city}</div>
                      <div><strong>Stadium:</strong> {selectedElement.stadium || 'Host Stadium'}</div>
                      <div><strong>Match:</strong> {selectedElement.match || 'Group Stage'}</div>
                      <div><strong>Date:</strong> {selectedElement.date}</div>
                      {selectedElement.team && <div><strong>Fan profile:</strong> {selectedElement.team} route marker</div>}
                      <div style={{ marginTop: '8px', padding: '8px', background: 'var(--c-background)', borderRadius: '6px', fontSize: '0.85rem' }}>
                        Welcome to {selectedElement.city}! Follow {selectedElement.team || 'the team'}'s journey to {selectedElement.stadium}.
                      </div>
                    </>
                  )}
                  {selectedElement.type === 'recommended' && (
                    <>
                      <div><strong>Recommended Stop</strong></div>
                      <div><strong>Stadium:</strong> {selectedElement.stadium || 'Host Stadium'}</div>
                    </>
                  )}
                </div>
              </div>
            )}

            <div style={{ position: 'absolute', top: '5px', right: '5px', background: 'rgba(0,0,0,0.7)', color: 'white', padding: '3px 8px', fontSize: '10px', borderRadius: '4px' }}>
              Fallback Mode (No API Key Required)
            </div>
          </div>
        )}
      </div>
    </MapContext.Provider>
  );
}
