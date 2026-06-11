import { useState, useEffect } from 'react';
import { getStadiums } from '../services/api';

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
        <p className="loading">Loading stadiums...</p>
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
        <section className="venue-grid">
          {stadiums.map((stadium, index) => (
            <article key={`${stadium.stadium}-${index}`} className="pitch-card">
              <div className="pitch-header">
                <div className="team-mark">
                  <span aria-hidden="true">26</span>
                  <strong>{stadium.city || 'Host city'}</strong>
                </div>
              </div>
              <div className="pitch-body">
                <strong>{stadium.stadium || '-'}</strong>
                <p className="description">
                  Capacity {stadium.capacity ? stadium.capacity.toLocaleString() : '-'}
                </p>
              </div>
            </article>
          ))}
        </section>
      )}
    </div>
  );
}
