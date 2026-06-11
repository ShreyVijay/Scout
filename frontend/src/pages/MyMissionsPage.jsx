import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getMissions } from '../services/api';
import { MissionBar } from '../components/PitchUI';
import { useSession } from '../store/useSession';

export default function MyMissionsPage() {
  const [missions, setMissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const email = useSession((state) => state.email);

  useEffect(() => {
    async function fetchAll() {
      try {
        const data = await getMissions(email);
        setMissions(data.missions || []);
      } catch (err) {
        setError(err.message || 'Failed to retrieve missions');
      } finally {
        setLoading(false);
      }
    }

    fetchAll();
  }, [email]);

  if (loading) {
    return (
      <div id="my-missions-page" className="page">
        <section className="page-header">
          <div>
            <p className="eyebrow">Operations board</p>
            <h1>My Travel Missions</h1>
          </div>
        </section>
        <div className="skeleton" style={{ height: '200px', marginBottom: '24px' }} />
        <div style={{ display: 'flex', gap: '16px' }}>
          <div className="skeleton" style={{ height: '140px', flex: 1 }} />
          <div className="skeleton" style={{ height: '140px', flex: 1 }} />
        </div>
      </div>
    );
  }

  const activeMission = missions.find(
    m => !['completed', 'cancelled', 'eliminated'].includes(m.mission_state)
  );
  const historyMissions = missions.filter(m => m !== activeMission);

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
        <div className="stagger">
          {activeMission && (
            <section style={{ marginBottom: '40px' }}>
              <h2 style={{ marginBottom: '16px', fontSize: '1.2rem' }}>Active Mission</h2>
              <article className="card" style={{ padding: '24px', border: '1px solid var(--c-amber-glow)' }}>
                <MissionBar mission={activeMission} />
                <div style={{ display: 'flex', gap: '24px', marginTop: '24px', alignItems: 'center' }}>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '0.8rem', color: 'var(--c-t2)', marginBottom: '4px' }}>Objective</div>
                    <div>{activeMission.objective || 'No objective set.'}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.8rem', color: 'var(--c-t2)', marginBottom: '4px' }}>Budget</div>
                    <strong style={{ fontSize: '1.2rem', color: 'var(--c-t1)' }}>
                      ${Number(activeMission.budget?.total_budget || activeMission.budget || 0).toLocaleString()}
                    </strong>
                  </div>
                </div>
                <div className="button-row" style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid var(--c-border)' }}>
                  <Link to={`/mission/${encodeURIComponent(activeMission.team)}`} className="btn">View Mission</Link>
                  <Link to={`/replan/${encodeURIComponent(activeMission.team)}`} className="btn btn-secondary">Replan Route</Link>
                </div>
              </article>
            </section>
          )}

          {historyMissions.length > 0 && (
            <section>
              <h2 style={{ marginBottom: '16px', fontSize: '1.2rem' }}>Past Missions</h2>
              <div className="data-grid">
                {historyMissions.map((mission, index) => {
                  const missionState = mission.mission_state || 'completed';
                  return (
                    <article key={`${mission.team}-${index}`} className="data-card" style={{ opacity: 0.65 }}>
                      <div className="section-title">
                        <strong>{mission.team}</strong>
                        <span className={`badge badge-${missionState}`}>{missionState.toUpperCase()}</span>
                      </div>
                      <p className="description">{mission.objective || 'No objective set.'}</p>
                      <div className="button-row" style={{ marginTop: '16px' }}>
                        <Link to={`/mission/${encodeURIComponent(mission.team)}`} className="btn btn-secondary btn-small">
                          View Log
                        </Link>
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          )}
        </div>
      )}
    </div>
  );
}
