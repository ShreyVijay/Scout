import { useState, useEffect } from 'react';
import { getCities } from '../services/api';

function ScoreLine({ label, value }) {
  const score = typeof value === 'number' ? value : 0;
  return (
    <div className="score-line">
      <span>{label}</span>
      <div className="score-bar" style={{ '--score': `${Math.min(score * 10, 100)}%` }}>
        <i />
      </div>
      <span className="mono">{value ?? '-'}</span>
    </div>
  );
}

export default function CitiesPage() {
  const [cities, setCities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchCities() {
      setLoading(true);
      setError(null);

      try {
        const data = await getCities();
        setCities(data.cities || []);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          err.message ||
          'Failed to load cities'
        );
      } finally {
        setLoading(false);
      }
    }

    fetchCities();
  }, []);

  if (loading) {
    return (
      <div id="cities-page" className="page">
        <h1>City Intelligence</h1>
        <p className="loading">Loading cities...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div id="cities-page" className="page">
        <h1>City Intelligence</h1>
        <div className="error-banner">{error}</div>
      </div>
    );
  }

  return (
    <div id="cities-page" className="page">
      <section className="page-header">
        <div>
          <p className="eyebrow">Tournament map</p>
          <h1>City Intelligence</h1>
        </div>
        <span className="badge">{cities.length} cities</span>
      </section>

      {cities.length === 0 ? (
        <p className="empty">No cities found.</p>
      ) : (
        <section className="venue-grid">
          {cities.map((city, index) => (
            <article key={`${city.city}-${index}`} className="venue-card">
              <strong>{city.city || '-'}</strong>
              <span>{city.country || 'Host market'}</span>
              <ScoreLine label="Atmosphere" value={city.atmosphere_score} />
              <ScoreLine label="Budget" value={city.budget_score} />
              <ScoreLine label="Transport" value={city.transport_score} />
              <ScoreLine label="Fan zone" value={city.fan_zone_score} />
            </article>
          ))}
        </section>
      )}
    </div>
  );
}
