import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getCityPhoto, searchHotels, searchFood } from '../services/placesService';
import MapView from './map/MapView';
import ItineraryMap from './map/ItineraryMap';
import { MapPin, ForkKnife, Bed, MapTrifold, Info } from '@phosphor-icons/react';

function ScoreLine({ label, value }) {
  const score = typeof value === 'number' ? value : 0;
  return (
    <div className="score-line" style={{ display: 'flex', alignItems: 'center', gap: '12px', fontSize: '0.85rem' }}>
      <span style={{ width: '80px', color: 'var(--c-t2)' }}>{label}</span>
      <div className="score-bar" style={{ flex: 1, height: '6px', background: 'var(--c-border)', borderRadius: '3px', overflow: 'hidden' }}>
        <i style={{ 
          display: 'block', 
          height: '100%', 
          background: 'var(--c-amber)', 
          borderRadius: '3px',
          '--score': `${Math.min(score * 10, 100)}%` 
        }} />
      </div>
      <span className="mono" style={{ width: '24px', textAlign: 'right' }}>{value ?? '-'}</span>
    </div>
  );
}

function PlaceCard({ place }) {
  return (
    <div style={{ display: 'flex', gap: '12px', padding: '12px 0', borderBottom: '1px solid var(--c-border)' }}>
      {place.photo_url ? (
        <img src={place.photo_url} alt={place.name} style={{ width: '60px', height: '60px', borderRadius: '8px', objectFit: 'cover' }} />
      ) : (
        <div style={{ width: '60px', height: '60px', borderRadius: '8px', background: 'var(--c-raised)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <MapPin color="var(--c-t2)" />
        </div>
      )}
      <div style={{ flex: 1 }}>
        <h4 style={{ margin: '0 0 4px', fontSize: '0.9rem', color: 'var(--c-t1)' }}>{place.name}</h4>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.8rem', color: 'var(--c-t2)' }}>
          <span>⭐ {place.rating}</span>
          <span>·</span>
          <span style={{ color: 'var(--c-green)' }}>{'$'.repeat(place.price_level)}</span>
        </div>
        <p style={{ margin: '4px 0 0', fontSize: '0.75rem', color: 'var(--c-t3)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '200px' }}>
          {place.vicinity}
        </p>
      </div>
    </div>
  );
}

export default function CityCard({ city }) {
  const [photoUrl, setPhotoUrl] = useState(null);
  const [loadingPhoto, setLoadingPhoto] = useState(true);
  
  const [activeTab, setActiveTab] = useState('overview');
  
  const [hotels, setHotels] = useState([]);
  const [loadingHotels, setLoadingHotels] = useState(false);
  const [food, setFood] = useState([]);
  const [loadingFood, setLoadingFood] = useState(false);

  // We need rough coords for nearby search if city coordinates aren't provided by backend.
  // We can fallback to MapView HOST_CITIES_COORDS or simple mapping.
  // Assuming city has lat/lng or we can just pass city.city
  
  const cityCoordsMap = {
    "Seattle": { lat: 47.6062, lng: -122.3321 },
    "Vancouver": { lat: 49.2827, lng: -123.1207 },
    "San Francisco": { lat: 37.7749, lng: -122.4194 },
    "Los Angeles": { lat: 34.0522, lng: -118.2437 },
    "Guadalajara": { lat: 20.6597, lng: -103.3496 },
    "Mexico City": { lat: 19.4326, lng: -99.1332 },
    "Monterrey": { lat: 25.6866, lng: -100.3161 },
    "Kansas City": { lat: 39.0997, lng: -94.5786 },
    "Dallas": { lat: 32.7767, lng: -96.7970 },
    "Houston": { lat: 29.7604, lng: -95.3698 },
    "Atlanta": { lat: 33.7490, lng: -84.3880 },
    "Miami": { lat: 25.7617, lng: -80.1918 },
    "Philadelphia": { lat: 39.9526, lng: -75.1652 },
    "Boston": { lat: 42.3601, lng: -71.0589 },
    "New York/New Jersey": { lat: 40.7128, lng: -74.0060 },
    "Toronto": { lat: 43.6532, lng: -79.3832 }
  };

  const coords = cityCoordsMap[city.city] || cityCoordsMap["Miami"];

  useEffect(() => {
    let mounted = true;
    async function loadPhoto() {
      if (city.city) {
        const url = await getCityPhoto(city.city);
        if (mounted && url) setPhotoUrl(url);
      }
      if (mounted) setLoadingPhoto(false);
    }
    loadPhoto();
    return () => { mounted = false; };
  }, [city.city]);

  useEffect(() => {
    if (activeTab === 'hotels' && hotels.length === 0) {
      setLoadingHotels(true);
      searchHotels(city.city, coords.lat, coords.lng).then(res => {
        setHotels(res);
        setLoadingHotels(false);
      });
    } else if (activeTab === 'eats' && food.length === 0) {
      setLoadingFood(true);
      searchFood(city.city, coords.lat, coords.lng).then(res => {
        setFood(res);
        setLoadingFood(false);
      });
    }
  }, [activeTab, city.city, coords.lat, coords.lng, hotels.length, food.length]);

  return (
    <article className="venue-card" style={{ padding: 0, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
      {/* Hero Image */}
      <div style={{ height: '140px', position: 'relative' }}>
        {loadingPhoto ? (
          <div className="skeleton" style={{ width: '100%', height: '100%', borderRadius: 0 }} />
        ) : photoUrl ? (
          <img src={photoUrl} alt={city.city} onError={() => setPhotoUrl(null)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        ) : (
          <div style={{ width: '100%', height: '100%', background: 'var(--c-surface)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: 'var(--c-t2)' }}>No image</span>
          </div>
        )}
        <div style={{ 
          position: 'absolute', bottom: 0, left: 0, right: 0, 
          padding: '16px 16px 12px',
          background: 'linear-gradient(to top, rgba(0,0,0,0.9), transparent)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
            <h3 style={{ margin: 0, color: 'white', fontSize: '1.25rem' }}>{city.city || '-'}</h3>
            <span style={{ color: '#ccc', fontSize: '0.85rem' }}>{city.country || 'Host'}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', borderBottom: '1px solid var(--c-border)', background: 'var(--c-raised)' }}>
        {[
          { id: 'overview', icon: <Info size={16} /> },
          { id: 'eats', icon: <ForkKnife size={16} /> },
          { id: 'hotels', icon: <Bed size={16} /> },
          { id: 'map', icon: <MapTrifold size={16} /> }
        ].map(t => (
          <button 
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            style={{ 
              flex: 1, 
              padding: '12px 0', 
              background: 'transparent', 
              border: 'none',
              borderBottom: activeTab === t.id ? '2px solid var(--c-amber)' : '2px solid transparent',
              color: activeTab === t.id ? 'var(--c-amber)' : 'var(--c-t2)',
              cursor: 'pointer',
              display: 'flex',
              justifyContent: 'center'
            }}
          >
            {t.icon}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ padding: '16px', flex: 1, background: 'var(--c-surface)', minHeight: '200px' }}>
        <AnimatePresence mode="wait">
          {activeTab === 'overview' && (
            <motion.div key="overview" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.15 }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <ScoreLine label="Atmosphere" value={city.atmosphere_score} />
                <ScoreLine label="Budget" value={city.budget_score} />
                <ScoreLine label="Transport" value={city.transport_score} />
                <ScoreLine label="Fan zone" value={city.fan_zone_score} />
              </div>
            </motion.div>
          )}

          {activeTab === 'eats' && (
            <motion.div key="eats" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.15 }}>
              {loadingFood ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {[1,2,3].map(i => <div key={i} className="skeleton" style={{ height: '60px' }} />)}
                </div>
              ) : food.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', maxHeight: '240px', overflowY: 'auto' }}>
                  {food.map((f, i) => <PlaceCard key={i} place={f} />)}
                </div>
              ) : (
                <p style={{ color: 'var(--c-t2)', textAlign: 'center', marginTop: '20px' }}>No food data found.</p>
              )}
            </motion.div>
          )}

          {activeTab === 'hotels' && (
            <motion.div key="hotels" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.15 }}>
              {loadingHotels ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {[1,2,3].map(i => <div key={i} className="skeleton" style={{ height: '60px' }} />)}
                </div>
              ) : hotels.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', maxHeight: '240px', overflowY: 'auto' }}>
                  {hotels.map((h, i) => <PlaceCard key={i} place={h} />)}
                </div>
              ) : (
                <p style={{ color: 'var(--c-t2)', textAlign: 'center', marginTop: '20px' }}>No hotel data found.</p>
              )}
            </motion.div>
          )}

          {activeTab === 'map' && (
            <motion.div key="map" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.15 }} style={{ height: '240px' }}>
              <MapView centerCity={city.city} height="100%">
                <ItineraryMap
                  team="skaut"
                  stops={[{
                    city: city.city,
                    stadium: city.stadium || 'Host city',
                    date: 'FIFA 2026',
                    match: `${city.city} host city`,
                  }]}
                />
              </MapView>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </article>
  );
}
