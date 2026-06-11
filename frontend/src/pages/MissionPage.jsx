import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getMission } from '../services/api';
import MissionCard from '../components/MissionCard';
import MissionStateCard from '../components/MissionStateCard';
import BudgetCard from '../components/BudgetCard';
import MapView from '../components/map/MapView';
import ItineraryMap from '../components/map/ItineraryMap';

export default function MissionPage() {
  const { team } = useParams();
  const [mission, setMission] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchMission() {
      setLoading(true);
      setError(null);

      try {
        const data = await getMission(team);
        setMission(data);
      } catch (err) {
        if (err.response?.status === 404) {
          setError(`Mission not found for team: ${team}`);
        } else {
          setError(
            err.response?.data?.detail ||
            err.message ||
            'Failed to load mission'
          );
        }
      } finally {
        setLoading(false);
      }
    }

    fetchMission();
  }, [team]);

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

  return (
    <div id="mission-page" className="page">
      <section className="page-header">
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

      <div className="grid-2">
        <MissionCard mission={mission} />
        <MissionStateCard mission={mission} />
      </div>

      <BudgetCard mission={mission} />

      {itinerary.length > 0 && (
        <section className="card" id="mission-itinerary-map">
          <div className="section-title">
            <h3>Itinerary Map</h3>
            <span className="badge">{itinerary.length} stops</span>
          </div>
          <MapView centerCity={itinerary[0]?.city} height="320px">
            <ItineraryMap stops={itinerary} />
          </MapView>
        </section>
      )}

      <section id="itinerary-section" className="card">
        <div className="section-title">
          <h3>Journey Timeline</h3>
        </div>
        {itinerary.length > 0 ? (
          <div className="timeline">
            {itinerary.map((item, index) => (
              <article key={`${item.city}-${index}`} className="timeline-item">
                <div className="timeline-node">{index + 1}</div>
                <div>
                  <strong>{item.city || '-'}</strong>
                  <small>{item.stadium || 'Stadium TBD'}</small>
                </div>
                <span className="badge">{item.date || 'TBD'}</span>
              </article>
            ))}
          </div>
        ) : (
          <p className="empty">No itinerary data.</p>
        )}
      </section>

      <section id="state-history-section" className="card">
        <div className="section-title">
          <h3>State History</h3>
          <span className="badge">{history.length} events</span>
        </div>
        {history.length > 0 ? (
          <div className="timeline">
            {history.map((entry, index) => (
              <article key={index} className="timeline-item">
                <div className="timeline-node">{index + 1}</div>
                <div>
                  <strong>{entry.event_type || entry.type || 'State change'}</strong>
                  <small>
                    {entry.from_stage || entry.from || '-'} to {entry.to_stage || entry.to || '-'}
                  </small>
                </div>
                <span className="badge">{entry.event_time || entry.timestamp || 'TBD'}</span>
              </article>
            ))}
          </div>
        ) : (
          <p className="empty">No state transitions recorded.</p>
        )}
      </section>
    </div>
  );
}
