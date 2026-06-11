import { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getMission } from '../services/api';
import MissionCard from '../components/MissionCard';
import MissionStateCard from '../components/MissionStateCard';
import BudgetCard from '../components/BudgetCard';
import MapView from '../components/map/MapView';
import ItineraryMap from '../components/map/ItineraryMap';
import { MissionBar, JourneyTimeline, HeroReplanning } from '../components/PitchUI';

export default function MissionPage() {
  const { team } = useParams();
  const [mission, setMission] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMission = useCallback(async (silent = false) => {
    if (!silent) setLoading(true);
    setError(null);

    try {
      const data = await getMission(team);
      setMission(data);
    } catch (err) {
      if (!silent) {
        if (err.response?.status === 404) {
          setError(`Mission not found for team: ${team}`);
        } else {
          setError(
            err.response?.data?.detail ||
            err.message ||
            'Failed to load mission'
          );
        }
      }
    } finally {
      if (!silent) setLoading(false);
    }
  }, [team]);

  useEffect(() => {
    fetchMission();
  }, [fetchMission]);

  // Poll every 5s to catch the 30-second elimination event
  useEffect(() => {
    const interval = setInterval(() => fetchMission(true), 5000);
    return () => clearInterval(interval);
  }, [fetchMission]);

  if (loading) {
    return (
      <div id="mission-page" className="page">
        <p className="loading">Loading mission...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div id="mission-page" className="page">
        <div className="error-banner">{error}</div>
      </div>
    );
  }

  if (!mission) {
    return (
      <div id="mission-page" className="page">
        <p className="empty">No data found.</p>
      </div>
    );
  }

  const itinerary = mission.itinerary || [];
  const history = mission.state_history || [];
  const isEliminated = mission.tournament_state === 'ELIMINATED' || mission.tournament_state === 'eliminated' || mission.mission_state === 'replanning_required';

  return (
    <div id="mission-page" className="map-layout">
      <MissionBar mission={mission} mode={isEliminated ? 'replanning' : 'monitoring'} />
      
      <div className="map-grid">
        <div className="map-sidebar">
          <section className="page-header" style={{ marginTop: 0 }}>
            <div>
              <p className="eyebrow">Mission control</p>
              <h1>{mission.team}</h1>
            </div>
            <Link
              to={`/replan/${encodeURIComponent(mission.team)}`}
              className="btn"
              id="link-replanning"
            >
              Review Route
            </Link>
          </section>

          {/* Elimination alert banner */}
          {isEliminated && (
            <section style={{ marginBottom: '16px' }}>
              <HeroReplanning
                team={mission.team}
                onReplan={() => window.location.href = `/replan/${encodeURIComponent(mission.team)}`}
                loading={false}
              />
            </section>
          )}

          <div className="grid-2">
            <MissionCard mission={mission} />
            <MissionStateCard mission={mission} />
          </div>

          <BudgetCard mission={mission} />

          {itinerary.length > 0 && (
            <section className="card" id="mission-itinerary-map">
              <div className="section-title">
                <h3>Itinerary Details</h3>
                <span className="badge">{itinerary.length} stops</span>
              </div>
              <JourneyTimeline itinerary={itinerary} />
            </section>
          )}

          {history.length > 0 && (
            <section className="card">
              <div className="section-title">
                <h3>Mission Logs</h3>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {history.map((evt, idx) => (
                  <div key={idx} style={{ 
                    padding: '0.75rem', 
                    background: 'var(--c-surface)', 
                    borderRadius: '8px',
                    borderLeft: `2px solid ${evt.state === 'eliminated' ? 'var(--c-red)' : 'var(--c-amber)'}`
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                      <strong style={{ fontSize: '0.85rem' }}>{evt.state.toUpperCase()}</strong>
                      <span style={{ fontSize: '0.75rem', color: 'var(--c-t3)' }}>
                        {new Date(evt.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                    {evt.reason && <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--c-t2)' }}>{evt.reason}</p>}
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>

        <div className="map-pane">
          <MapView centerCity={itinerary[0]?.city || 'Miami'} height="100%">
            <ItineraryMap stops={itinerary} team={mission.team} />
          </MapView>
        </div>
      </div>
    </div>
  );
}
