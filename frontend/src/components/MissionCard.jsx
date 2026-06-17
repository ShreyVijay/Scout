// MissionCard.jsx

export default function MissionCard({ mission }) {
  if (!mission) return null;

  return (
    <section id="mission-card" className="pitch-card">
      <div className="pitch-header">
        <div className="matchup">
          <div className="team-mark">
            <span aria-hidden="true">BR</span>
            <strong>{mission.team || 'Team'}</strong>
          </div>
          <div>
            <div className="vs-mark">MISSION</div>
            <span className="badge">{mission.travel_style || 'travel'}</span>
          </div>
          <div className="team-mark">
            <span aria-hidden="true">26</span>
            <strong>World Cup</strong>
          </div>
        </div>
      </div>
      <div className="pitch-body">
        <div className="section-title">
          <h3>Mission Overview</h3>
          <span className="badge">{mission.mission_id || 'draft'}</span>
        </div>
        <p className="description">{mission.objective || 'No objective defined yet.'}</p>
      </div>
    </section>
  );
}
