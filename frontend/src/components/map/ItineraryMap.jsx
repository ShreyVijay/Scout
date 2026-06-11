// frontend/src/components/map/ItineraryMap.jsx
import { useContext, useEffect, useRef } from 'react';
import { MapContext } from './MapView';

export default function ItineraryMap({ stops = [], team }) {
  const context = useContext(MapContext);
  const markersRef = useRef([]);
  const polylineRef = useRef(null);

  useEffect(() => {
    if (!context) return;
    const { googleMapsLoaded, mapInstance, registerMarker, unregisterMarker, registerPath, unregisterPath, cityCoordsMap } = context;

    // Clear previous refs
    markersRef.current.forEach(m => {
      if (typeof m.setMap === 'function') m.setMap(null);
    });
    markersRef.current = [];

    if (polylineRef.current) {
      if (typeof polylineRef.current.setMap === 'function') polylineRef.current.setMap(null);
      polylineRef.current = null;
    }

    const fallbackStops = [
      { city: 'Mexico City', stadium: 'Estadio Azteca', date: '2026-06-11', match: 'Opening match' },
      { city: 'Toronto', stadium: 'BMO Field', date: '2026-06-12', match: 'Group stage' },
      { city: 'Los Angeles', stadium: 'SoFi Stadium', date: '2026-06-12', match: 'Group stage' },
      { city: 'Dallas', stadium: 'AT&T Stadium', date: '2026-06-20', match: 'Host city' },
      { city: 'New York/New Jersey', stadium: 'MetLife Stadium', date: '2026-07-19', match: 'Final' },
    ];
    const visibleStops = stops && stops.length > 0 ? stops : fallbackStops;

    if (googleMapsLoaded && mapInstance) {
      // Real Google Maps logic
      const pathCoords = [];
      const bounds = new window.google.maps.LatLngBounds();

      visibleStops.forEach((stop, index) => {
        const cityInfo = cityCoordsMap[stop.city];
        if (!cityInfo) return;

        const pos = { lat: cityInfo.lat, lng: cityInfo.lng };
        pathCoords.push(pos);
        bounds.extend(pos);

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="color: #1a1a2e; padding: 4px;">
              <h4 style="margin: 0 0 4px 0;">Stop ${index + 1}: ${stop.city}</h4>
              <p style="margin: 0; font-size: 11px;">
                <strong>Stadium:</strong> ${stop.stadium || 'Host Stadium'}<br/>
                <strong>Date:</strong> ${stop.date}
              </p>
            </div>
          `
        });

        const marker = new window.google.maps.Marker({
          position: pos,
          map: mapInstance,
          title: `Stop ${index + 1}: ${stop.city}`,
          label: (index + 1).toString(),
          icon: {
            path: window.google.maps.SymbolPath.CIRCLE,
            fillColor: '#2d6a4f',
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 2,
            scale: 10
          }
        });

        marker.addListener('click', () => {
          infoWindow.open(mapInstance, marker);
        });

        markersRef.current.push(marker);
      });

      // Draw polyline connecting stops
      if (pathCoords.length >= 2) {
        const poly = new window.google.maps.Polyline({
          path: pathCoords,
          geodesic: true,
          strokeColor: '#2d6a4f',
          strokeOpacity: 0.8,
          strokeWeight: 4,
          map: mapInstance
        });
        polylineRef.current = poly;
        mapInstance.fitBounds(bounds);
      }
    } else {
      // Fallback custom SVG map registration
      visibleStops.forEach((stop, index) => {
        registerMarker({
          id: `stop-${stop.city}-${index}`,
          type: 'city',
          city: stop.city,
          name: `Stop ${index + 1}: ${stop.city}`,
          stadium: stop.stadium || 'Host Stadium',
          date: stop.date,
          match: stop.match || `Tournament Stop #${index + 1}`,
          team: team
        });
      });

      if (visibleStops.length >= 2) {
        registerPath({
          id: 'itinerary-path',
          stops: visibleStops.map(s => s.city),
          color: '#2d6a4f'
        });
      }

      // Cleanup registration
      return () => {
        visibleStops.forEach((stop, index) => {
          unregisterMarker(`stop-${stop.city}-${index}`);
        });
        unregisterPath('itinerary-path');
      };
    }
  }, [stops, context]);

  return null;
}
