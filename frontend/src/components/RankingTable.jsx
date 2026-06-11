export default function RankingTable({ rankings }) {
  if (!rankings || rankings.length === 0) {
    return (
      <section id="ranking-table" className="card">
        <h3>Rankings</h3>
        <p className="empty">No rankings available.</p>
      </section>
    );
  }

  return (
    <section id="ranking-table" className="card">
      <div className="section-title">
        <h3>Rankings</h3>
        <span className="badge">{rankings.length} candidates</span>
      </div>
      <div className="data-grid">
        {rankings.map((ranking, index) => {
          const score =
            typeof ranking.final_score === 'number'
              ? ranking.final_score.toFixed(2)
              : '-';
          const scoreWidth =
            typeof ranking.final_score === 'number'
              ? `${Math.min(Math.max(ranking.final_score * 10, 8), 100)}%`
              : '0%';

          return (
            <article key={`${ranking.city}-${index}`} className="data-card">
              <strong>#{ranking.rank ?? index + 1} {ranking.city || '-'}</strong>
              <span>{ranking.candidate_source || 'Candidate'}</span>
              <div className="score-line">
                <div className="score-bar" style={{ '--score': scoreWidth }}>
                  <i />
                </div>
                <span className="mono">{score}</span>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}
