import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getMissions } from '../services/api';
import WalletDrawer from '../components/WalletDrawer';
import { useWallet } from '../store/useWallet';
import { useSession } from '../store/useSession';
import { t } from '../i18n';
import { HeroLive, GoalOverlay } from '../components/PitchUI';

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
  const [walletOpen, setWalletOpen] = useState(false);
  const language = useSession((state) => state.language);
  const balance = useWallet((state) => state.balance);
  const [goalVisible, setGoalVisible] = useState(false);

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

  const activeMissionsCount = missions.length;
  const savedRecsCount = savedRecs.length;

  function removeRecommendation(index) {
    const updated = savedRecs.filter((_, i) => i !== index);
    localStorage.setItem('saved_recommendations', JSON.stringify(updated));
    setSavedRecs(updated);
  }

  return (
    <div id="dashboard-page" className="page">
      <section className="hero-section">
        <p className="eyebrow">{t('dashboard.hero_eyebrow', language)}</p>
        <h1 className="hero-title">{t('dashboard.hero_title', language)}</h1>
      </section>

      <section className="stats-grid">
        <article className="stat-card">
          <p className="stat-label">{t('dashboard.active_missions', language)}</p>
          <p className="stat-value">{activeMissionsCount}</p>
        </article>
        <article className="stat-card" onClick={() => setWalletOpen(true)} style={{ cursor: 'pointer' }}>
          <p className="stat-label">{t('dashboard.budget_tracked', language)}</p>
          <p className="stat-value">${balance.toLocaleString()}</p>
        </article>
        <article className="stat-card">
          <p className="stat-label">{t('dashboard.saved_recs', language)}</p>
          <p className="stat-value">{savedRecsCount}</p>
        </article>
      </section>

      <WalletDrawer open={walletOpen} onClose={() => setWalletOpen(false)} />

      <section style={{ marginBottom: '24px' }}>
        <HeroLive onGoal={() => setGoalVisible(true)} />
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

      <GoalOverlay
        visible={goalVisible}
        scorer="Brazil route momentum changed"
        onDismiss={() => setGoalVisible(false)}
      />
    </div>
  );
}
