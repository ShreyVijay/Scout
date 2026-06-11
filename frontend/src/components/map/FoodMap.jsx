// frontend/src/components/map/FoodMap.jsx
import { useContext, useEffect, useRef } from 'react';
import { MapContext } from './MapView';

export default function FoodMap({ venues = [], city = "Miami" }) {
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

    if (!venues || venues.length === 0) return;

    if (googleMapsLoaded && mapInstance) {
      // Real Google maps implementation
      venues.forEach((venue, idx) => {
        const centerCoords = cityCoordsMap[city] || cityCoordsMap["Miami"];
        
        // Jitter lat/lng slightly from center to spread food markers on Google Map
        const jitterLat = ((idx * 19 + 7) % 13 - 6) * 0.0035;
        const jitterLng = ((idx * 29 + 11) % 13 - 6) * 0.0035;
        const pos = { lat: centerCoords.lat + jitterLat, lng: centerCoords.lng + jitterLng };

        const infoWindow = new window.google.maps.InfoWindow({
          content: `
            <div style="color: #1a1a2e; padding: 4px;">
              <h4 style="margin: 0 0 4px 0;">🍔 ${venue.name}</h4>
              <p style="margin: 0; font-size: 11px;">
                <strong>Category:</strong> ${venue.category}<br/>
                <strong>Rating:</strong> ⭐ ${venue.rating}<br/>
                <strong>Price Level:</strong> ${'$'.repeat(venue.price_level)}<br/>
                <strong>Address:</strong> ${venue.address}
              </p>
            </div>
          `
        });

        const marker = new window.google.maps.Marker({
          position: pos,
          map: mapInstance,
          title: venue.name,
          icon: {
            path: window.google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
            fillColor: '#dc3545',
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
      venues.forEach((venue, idx) => {
        registerMarker({
          id: `food-${city}-${idx}-${venue.name}`,
          type: 'food',
          city,
          name: venue.name,
          rating: venue.rating,
          category: venue.category,
          price_level: venue.price_level,
          address: venue.address
        });
      });

      return () => {
        venues.forEach((venue, idx) => {
          unregisterMarker(`food-${city}-${idx}-${venue.name}`);
        });
      };
    }
  }, [venues, city, context]);

  return null;
}
