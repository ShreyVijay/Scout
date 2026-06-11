import { useState, useEffect } from 'react';
import { getCities } from '../services/api';
import CityCard from '../components/CityCard';

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
        <section className="venue-grid stagger">
          {[1,2,3,4].map(i => <div key={i} className="skeleton" style={{ height: '360px' }} />)}
        </section>
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
        <section className="venue-grid stagger">
          {cities.map((city, index) => (
            <CityCard key={`${city.city}-${index}`} city={city} />
          ))}
        </section>
      )}
    </div>
  );
}
