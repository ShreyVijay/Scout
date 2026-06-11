import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getStadiums } from '../services/api';
import { getStadiumPhoto } from '../services/placesService';
import { MapPin, Users } from '@phosphor-icons/react';
import MapView from '../components/map/MapView';
import ItineraryMap from '../components/map/ItineraryMap';

function StadiumCard({ stadium }) {
  const [photoUrl, setPhotoUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    let mounted = true;
    async function loadPhoto() {
      if (stadium.stadium) {
        const url = await getStadiumPhoto(stadium.stadium);
        if (mounted && url) {
          setPhotoUrl(url);
        }
      }
      if (mounted) setLoading(false);
    }
    loadPhoto();
    return () => { mounted = false; };
  }, [stadium.stadium]);

  return (
    <motion.article 
      layout
      onClick={() => setExpanded(!expanded)}
      className="venue-card" 
      style={{ cursor: 'pointer', overflow: 'hidden', padding: 0, display: 'flex', flexDirection: 'column' }}
    >
      <div style={{ height: '160px', width: '100%', position: 'relative' }}>
        {loading ? (
          <div className="skeleton" style={{ width: '100%', height: '100%', borderRadius: '0' }} />
        ) : photoUrl ? (
          <img
            src={photoUrl} 
            alt={stadium.stadium} 
            onError={() => setPhotoUrl(null)}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
          />
        ) : (
          <div style={{ width: '100%', height: '100%', background: 'var(--c-surface)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <span style={{ color: 'var(--c-t2)' }}>No image</span>
          </div>
        )}
        <div style={{ 
          position: 'absolute', 
          bottom: 0, left: 0, right: 0, 
          padding: '12px', 
          background: 'linear-gradient(to top, rgba(0,0,0,0.8), transparent)' 
        }}>
          <h3 style={{ margin: 0, color: 'white' }}>{stadium.stadium}</h3>
          <p style={{ margin: 0, fontSize: '0.8rem', color: '#ccc', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <MapPin size={14} /> {stadium.city || 'Host city'}
          </p>
        </div>
      </div>
      
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            style={{ overflow: 'hidden', padding: '16px', background: 'var(--c-surface)' }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--c-t2)', marginBottom: '8px' }}>
              <Users size={16} /> Capacity: <strong style={{ color: 'var(--c-t1)' }}>{stadium.capacity ? stadium.capacity.toLocaleString() : '-'}</strong>
            </div>
            {/* Can add more stadium details here later */}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.article>
  );
}

export default function StadiumsPage() {
  const [stadiums, setStadiums] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchStadiums() {
      setLoading(true);
      setError(null);

      try {
        const data = await getStadiums();
        setStadiums(data.stadiums || []);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          err.message ||
          'Failed to load stadiums'
        );
      } finally {
        setLoading(false);
      }
    }

    fetchStadiums();
  }, []);

  if (loading) {
    return (
      <div id="stadiums-page" className="page">
        <h1>Stadiums</h1>
        <section className="venue-grid stagger">
          {[1,2,3,4,5,6].map(i => <div key={i} className="skeleton" style={{ height: '240px' }} />)}
        </section>
      </div>
    );
  }

  if (error) {
    return (
      <div id="stadiums-page" className="page">
        <h1>Stadiums</h1>
        <div className="error-banner">{error}</div>
      </div>
    );
  }

  return (
    <div id="stadiums-page" className="page">
      <section className="page-header">
        <div>
          <p className="eyebrow">Venue book</p>
          <h1>Stadiums</h1>
        </div>
        <span className="badge">{stadiums.length} venues</span>
      </section>

      {stadiums.length === 0 ? (
        <p className="empty">No stadiums found.</p>
      ) : (
        <>
          <section className="card map-section">
            <div className="section-title">
              <div>
                <p className="eyebrow">Map</p>
                <h2>Stadiums & Host Cities</h2>
              </div>
              <span className="badge">{stadiums.length} markers</span>
            </div>
            <div className="map-section-frame">
              <MapView centerCity={stadiums[0]?.city || 'Mexico City'} height="100%">
                <ItineraryMap
                  team="skaut"
                  stops={stadiums.map((stadium) => ({
                    city: stadium.city,
                    stadium: stadium.stadium,
                    date: stadium.capacity ? `${Number(stadium.capacity).toLocaleString()} capacity` : 'FIFA 2026 venue',
                    match: `${stadium.stadium} - ${stadium.city}`,
                  }))}
                />
              </MapView>
            </div>
          </section>

          <section className="venue-grid stagger">
            {stadiums.map((stadium, index) => (
              <StadiumCard key={`${stadium.stadium}-${index}`} stadium={stadium} />
            ))}
          </section>
        </>
      )}
    </div>
  );
}
