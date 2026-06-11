// frontend/src/components/map/DirectionsRoute.jsx
import { useContext, useEffect, useRef } from 'react';
import { MapContext } from './MapView';

export default function DirectionsRoute({ startCity, endCity }) {
  const context = useContext(MapContext);
  const lineRef = useRef(null);
  const startMarkerRef = useRef(null);
  const endMarkerRef = useRef(null);

  useEffect(() => {
    if (!context) return;
    const { googleMapsLoaded, mapInstance, registerPath, unregisterPath, registerMarker, unregisterMarker, cityCoordsMap } = context;

    // Clean up previous elements
    if (lineRef.current) {
      if (typeof lineRef.current.setMap === 'function') lineRef.current.setMap(null);
      lineRef.current = null;
    }
    if (startMarkerRef.current) {
      if (typeof startMarkerRef.current.setMap === 'function') startMarkerRef.current.setMap(null);
      startMarkerRef.current = null;
    }
    if (endMarkerRef.current) {
      if (typeof endMarkerRef.current.setMap === 'function') endMarkerRef.current.setMap(null);
      endMarkerRef.current = null;
    }

    if (!startCity || !endCity) return;

    if (googleMapsLoaded && mapInstance) {
      const startCoords = cityCoordsMap[startCity];
      const endCoords = cityCoordsMap[endCity];

      if (startCoords && endCoords) {
        const startPos = { lat: startCoords.lat, lng: startCoords.lng };
        const endPos = { lat: endCoords.lat, lng: endCoords.lng };

        // Create start marker
        startMarkerRef.current = new window.google.maps.Marker({
          position: startPos,
          map: mapInstance,
          title: `Start: ${startCity}`,
          icon: {
            path: window.google.maps.SymbolPath.CIRCLE,
            fillColor: '#7f8c8d',
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 2,
            scale: 8
          }
        });

        // Create end marker
        endMarkerRef.current = new window.google.maps.Marker({
          position: endPos,
          map: mapInstance,
          title: `Destination: ${endCity}`,
          icon: {
            path: window.google.maps.SymbolPath.CIRCLE,
            fillColor: '#e67e22',
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 2,
            scale: 10
          }
        });

        // Draw geodesic route line
        lineRef.current = new window.google.maps.Polyline({
          path: [startPos, endPos],
          geodesic: true,
          strokeColor: '#e67e22',
          strokeOpacity: 0.8,
          strokeWeight: 3.5,
          map: mapInstance
        });

        const bounds = new window.google.maps.LatLngBounds();
        bounds.extend(startPos);
        bounds.extend(endPos);
        mapInstance.fitBounds(bounds);
      }
    } else {
      // Fallback SVG registration
      registerMarker({
        id: `dir-start-${startCity}`,
        type: 'city',
        city: startCity,
        name: `Current Location: ${startCity}`,
        stadium: 'Starting Location',
        date: 'Departure Stop'
      });

      registerMarker({
        id: `dir-end-${endCity}`,
        type: 'recommended',
        city: endCity,
        name: `Recommended Destination: ${endCity}`,
        stadium: 'Host Venue Stadium'
      });

      registerPath({
        id: 'directions-path',
        type: 'directions',
        startCity,
        endCity,
        color: '#e67e22'
      });

      return () => {
        unregisterMarker(`dir-start-${startCity}`);
        unregisterMarker(`dir-end-${endCity}`);
        unregisterPath('directions-path');
      };
    }
  }, [startCity, endCity, context]);

  return null;
}
