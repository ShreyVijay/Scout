// frontend/src/components/map/HotelMap.jsx
import { useContext, useEffect, useRef } from 'react';
import { MapContext } from './MapView';

export default function HotelMap({ hotels = [], city = "Miami" }) {
  const context = useContext(MapContext);
  const markersRef = useRef([]);

  useEffect(() => {
    if (!context) return;
    const { googleMapsLoaded, mapInstance, registerMarker, unregisterMarker, cityCoordsMap } = context;

    // Clear previous Google markers
    markersRef.current.forEach(m => {
      if (typeof m.setMap === 'function') m.setMap(null);
    });
    markersRef.current = [];

    if (!hotels || hotels.length === 0) return;

    if (googleMapsLoaded && mapInstance) {
      // Real Google maps implementation
      hotels.forEach((hotel, idx) => {
        const centerCoords = cityCoordsMap[city] || cityCoordsMap["Miami"];
        
        // Jitter lat/lng slightly from center to spread hotel markers on Google Map
        const jitterLat = ((idx * 17) % 11 - 5) * 0.003;
        const jitterLng = ((idx * 23) % 11 - 5) * 0.003;
        const pos = { lat: centerCoords.lat + jitterLat, lng: centerCoords.lng + jitterLng };

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="color: #1a1a2e; padding: 4px;">
              <h4 style="margin: 0 0 4px 0;">🏨 ${hotel.name}</h4>
              <p style="margin: 0; font-size: 11px;">
                <strong>Rating:</strong> ⭐ ${hotel.rating}<br/>
                <strong>Price Level:</strong> ${'$'.repeat(hotel.price_level)}<br/>
                <strong>Distance:</strong> ${hotel.distance}<br/>
                <strong>Address:</strong> ${hotel.address}
              </p>
            </div>
          `
        });

        const marker = new window.google.maps.Marker({
          position: pos,
          map: mapInstance,
          title: hotel.name,
          icon: {
            path: window.google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
            fillColor: '#0d6efd',
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 1.5,
            scale: 6
          }
        });

        marker.addListener('click', () => {
          infoWindow.open(mapInstance, marker);
        });

        markersRef.current.push(marker);
      });
    } else {
      // Fallback SVG map registration
      hotels.forEach((hotel, idx) => {
        registerMarker({
          id: `hotel-${city}-${idx}-${hotel.name}`,
          type: 'hotel',
          city,
          name: hotel.name,
          rating: hotel.rating,
          price_level: hotel.price_level,
          distance: hotel.distance,
          address: hotel.address
        });
      });

      return () => {
        hotels.forEach((hotel, idx) => {
          unregisterMarker(`hotel-${city}-${idx}-${hotel.name}`);
        });
      };
    }
  }, [hotels, city, context]);

  return null;
}
