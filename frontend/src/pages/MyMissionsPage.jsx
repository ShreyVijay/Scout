import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getMissions } from '../services/api';

export default function MyMissionsPage() {
  const [missions, setMissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchAll() {
      try {
        const data = await getMissions();
        setMissions(data.missions || []);
      } catch (err) {
        setError(err.message || 'Failed to retrieve missions');
      } finally {
        setLoading(false);
      }
    }

    fetchAll();
  }, []);

  if (loading) {
    return (
      <div id="my-missions-page" className="page">
        <p className="loading">Loading missions list...</p>
      </div>
    );
  }

  return (
    <div id="my-missions-page" className="page">
      <section className="page-header">
        <div>
          <p className="eyebrow">Operations board</p>
          <h1>My Travel Missions</h1>
        </div>
        <Link to="/new-mission" className="btn">Create Mission</Link>
      </section>

      {error && <div className="error-banner">{error}</div>}

      {missions.length === 0 ? (
        <section className="card">
          <p className="empty">You have no active or planned missions.</p>
          <Link to="/new-mission" className="btn">Setup Your First Mission</Link>
        </section>
      ) : (
        <section className="data-grid">
          {missions.map((mission, index) => {
            const missionState = mission.mission_state || 'planned';
            const tournamentState = mission.tournament_state || 'group_stage';
            return (
              <article key={`${mission.team}-${index}`} className="data-card">
                <div className="section-title">
                  <strong>{mission.team}</strong>
                  <span className={`badge badge-${missionState}`}>{missionState}</span>
                </div>
                <p className="description">{mission.objective || 'No objective set.'}</p>
                <div className="status-strip">
                  <div className="status-cell">
                    <strong>${Number(mission.budget?.total_budget || mission.budget || 0).toLocaleString()}</strong>
                    <span>Budget</span>
                  </div>
                  <div className="status-cell">
                    <strong>{mission.travel_style || '-'}</strong>
                    <span>Style</span>
                  </div>
                  <div className="status-cell">
                    <strong>{tournamentState.replace('_', ' ')}</strong>
                    <span>Stage</span>
                  </div>
                </div>
                <div className="button-row">
                  <Link to={`/mission/${encodeURIComponent(mission.team)}`} className="btn btn-small">
                    View
                  </Link>
                  <Link to={`/replan/${encodeURIComponent(mission.team)}`} className="btn btn-secondary btn-small">
                    Replan
                  </Link>
                </div>
              </article>
            );
          })}
        </section>
      )}
    </div>
  );
}
