export default function MissionStateCard({ mission }) {
  if (!mission) return null;

  const missionState = mission.mission_state || 'planned';
  const tournamentState = mission.tournament_state || 'group_stage';
  const requiresReplanning =
    missionState === 'monitoring' ||
    missionState === 'replanning';

  return (
    <section id="mission-state-card" className="card">
      <div className="section-title">
        <h3>Mission State</h3>
        <span className={`badge badge-${missionState}`}>{missionState}</span>
      </div>

      <div className="status-strip">
        <div className="status-cell">
          <strong>{missionState.replace('_', ' ')}</strong>
          <span>Mission</span>
        </div>
        <div className="status-cell">
          <strong>{tournamentState.replace('_', ' ')}</strong>
          <span>Tournament</span>
        </div>
        <div className="status-cell">
          <strong>{requiresReplanning ? 'Yes' : 'No'}</strong>
          <span>Replan</span>
        </div>
      </div>
    </section>
  );
}
