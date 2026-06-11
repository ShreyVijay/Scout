import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getMissions } from '../services/api';

const alerts = [
  {
    id: 1,
    type: 'warning',
    text: 'Road closures and heavy delays expected near Hard Rock Stadium due to local operations.',
    date: 'June 10, 2026',
  },
  {
    id: 2,
    type: 'info',
    text: 'Flight prices from New York to Seattle have dropped by 12% today.',
    date: 'June 9, 2026',
  },
  {
    id: 3,
    type: 'success',
    text: 'Fresh allocation of group stage category 3 tickets released for Seattle matches.',
    date: 'June 8, 2026',
  },
];

export default function DashboardPage() {
  const [missions, setMissions] = useState([]);
  const [savedRecs, setSavedRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadDashboard() {
      setLoading(true);
      setError(null);

      try {
        const data = await getMissions();
        setMissions(data.missions || []);
      } catch (err) {
        setError(err.message || 'Failed to fetch missions');
      } finally {
        setLoading(false);
      }

      try {
        const saved = JSON.parse(localStorage.getItem('saved_recommendations') || '[]');
        setSavedRecs(saved);
      } catch {
        setSavedRecs([]);
      }
    }

    loadDashboard();
  }, []);

  const totalBudget = missions.reduce((sum, mission) => {
    const value = mission.budget?.total_budget || mission.budget || 0;
    return sum + Number(value || 0);
  }, 0);

  function removeRecommendation(index) {
    const updated = savedRecs.filter((_, i) => i !== index);
    localStorage.setItem('saved_recommendations', JSON.stringify(updated));
    setSavedRecs(updated);
  }

  return (
    <div id="dashboard-page" className="page">
      <section className="dashboard-hero">
        <div>
          <p className="eyebrow">Scout command center</p>
          <h1>Plan every match-day move before the table changes.</h1>
          <p>
            Track missions, budget exposure, saved routes, and live travel signals
            for FIFA 2026 trips.
          </p>
        </div>
        <Link to="/new-mission" className="btn">Create Mission</Link>
      </section>

      <section className="metric-grid" aria-label="Dashboard metrics">
        <div className="metric-tile">
          <span>Active missions</span>
          <strong>{missions.length}</strong>
        </div>
        <div className="metric-tile">
          <span>Budget tracked</span>
          <strong>${totalBudget.toLocaleString()}</strong>
        </div>
        <div className="metric-tile">
          <span>Saved recommendations</span>
          <strong>{savedRecs.length}</strong>
        </div>
      </section>

      <div className="grid-2">
        <section className="card">
          <div className="section-title">
            <h2>Recent Missions</h2>
            {missions.length > 5 && <Link to="/my-missions">See all</Link>}
          </div>

          {loading ? (
            <p className="loading">Loading missions...</p>
          ) : error ? (
            <div className="error-banner">{error}</div>
          ) : missions.length === 0 ? (
            <div>
              <p className="empty">No missions created yet.</p>
              <Link to="/new-mission" className="btn btn-secondary">Create Mission</Link>
            </div>
          ) : (
            <div className="mission-list">
              {missions.slice(-5).reverse().map((mission, index) => (
                <Link
                  key={`${mission.team}-${index}`}
                  className="mission-row"
                  to={`/mission/${encodeURIComponent(mission.team)}`}
                >
                  <span>
                    <strong>{mission.team}</strong>
                    <small>{mission.objective || 'Follow the tournament path'}</small>
                  </span>
                  <span className="mission-meta">
                    <span className="badge">{mission.travel_style}</span>
                    <strong>${Number(mission.budget?.total_budget || mission.budget || 0).toLocaleString()}</strong>
                  </span>
                </Link>
              ))}
            </div>
          )}
        </section>

        <section className="card">
          <div className="section-title">
            <h2>Intelligence Alerts</h2>
          </div>
          <div className="alert-stack">
            {alerts.map((alert) => (
              <article key={alert.id} className={`alert-item alert-${alert.type}`}>
                <div>
                  <span>{alert.type}</span>
                  <time>{alert.date}</time>
                </div>
                <p>{alert.text}</p>
              </article>
            ))}
          </div>
        </section>
      </div>

      <section className="card">
        <div className="section-title">
          <h2>Saved Recommendations</h2>
        </div>
        {savedRecs.length === 0 ? (
          <p className="empty">No recommendations saved yet. Generate one to save it to your dashboard.</p>
        ) : (
          <div className="grid-2">
            {savedRecs.map((rec, index) => (
              <article key={`${rec.city}-${index}`} className="recommendation-tile">
                <h3>{rec.city}</h3>
                <p>
                  <strong>Match:</strong> {rec.match || '-'}<br />
                  <strong>Reason:</strong> {rec.reason || '-'}<br />
                  <strong>Score:</strong> {rec.final_score || rec.score || '-'}
                </p>
                <div className="button-row">
                  <Link to={`/replan/${encodeURIComponent(rec.team || 'Egypt')}`} className="btn btn-small">
                    Replan
                  </Link>
                  <button
                    type="button"
                    className="btn btn-secondary btn-small"
                    onClick={() => removeRecommendation(index)}
                  >
                    Remove
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
