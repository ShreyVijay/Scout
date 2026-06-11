export default function RecommendationCard({ recommendation }) {
  if (!recommendation) {
    return (
      <section id="recommendation-card" className="card">
        <h3>Recommendation</h3>
        <p className="empty">No recommendation generated yet.</p>
      </section>
    );
  }

  const rawScore =
    typeof recommendation.raw_score === 'number'
      ? recommendation.raw_score.toFixed(2)
      : '-';
  const finalScore =
    typeof recommendation.final_score === 'number'
      ? recommendation.final_score.toFixed(2)
      : '-';

  return (
    <section id="recommendation-card" className="pitch-card">
      <div className="pitch-header">
        <div>
          <p className="eyebrow">Recommended destination</p>
          <h2>{recommendation.city || 'Unknown city'}</h2>
        </div>
      </div>
      <div className="pitch-body">
        <div className="data-grid">
          <div className="data-card">
            <strong>{recommendation.match || '-'}</strong>
            <span>Match</span>
          </div>
          <div className="data-card">
            <strong>{recommendation.candidate_source || '-'}</strong>
            <span>Candidate source</span>
          </div>
          <div className="data-card">
            <strong>#{recommendation.rank ?? '-'}</strong>
            <span>Rank</span>
          </div>
        </div>
        <div className="status-strip" style={{ marginTop: '1rem' }}>
          <div className="status-cell">
            <strong>{rawScore}</strong>
            <span>Raw score</span>
          </div>
          <div className="status-cell">
            <strong>{finalScore}</strong>
            <span>Final score</span>
          </div>
          <div className="status-cell">
            <strong>{recommendation.reason ? 'Ready' : 'Scored'}</strong>
            <span>Decision</span>
          </div>
        </div>
      </div>
    </section>
  );
}
