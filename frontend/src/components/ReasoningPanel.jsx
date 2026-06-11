export default function ReasoningPanel({ reasoning }) {
  if (!reasoning) {
    return (
      <div id="reasoning-panel" className="card">
        <h3>Reasoning</h3>
        <p className="empty">No reasoning available.</p>
      </div>
    );
  }

  return (
    <div id="reasoning-panel" className="card">
      <h3>Reasoning</h3>

      <table>
        <tbody>
          <tr>
            <td className="label">Decision</td>
            <td><strong>{reasoning.decision || '—'}</strong></td>
          </tr>
          <tr>
            <td className="label">Source</td>
            <td>{reasoning.candidate_source || '—'}</td>
          </tr>
          <tr>
            <td className="label">Source Multiplier</td>
            <td>
              {typeof reasoning.source_multiplier === 'number'
                ? reasoning.source_multiplier.toFixed(2)
                : '—'}
            </td>
          </tr>
          <tr>
            <td className="label">Final Score</td>
            <td>
              {typeof reasoning.final_score === 'number'
                ? reasoning.final_score.toFixed(2)
                : '—'}
            </td>
          </tr>
        </tbody>
      </table>

      {reasoning.top_factors && reasoning.top_factors.length > 0 && (
        <div className="sub-section">
          <h4>Top Factors</h4>
          <ul>
            {reasoning.top_factors.map((factor, idx) => (
              <li key={idx}>{factor}</li>
            ))}
          </ul>
        </div>
      )}

      {reasoning.contributions && (
        <div className="sub-section">
          <h4>Contributions</h4>
          <table>
            <tbody>
              {Object.entries(reasoning.contributions).map(([key, val]) => (
                <tr key={key}>
                  <td className="label">{key}</td>
                  <td>{typeof val === 'number' ? val.toFixed(2) : val}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {reasoning.reasons && reasoning.reasons.length > 0 && (
        <div className="sub-section">
          <h4>Reasons</h4>
          <ul>
            {reasoning.reasons.map((reason, idx) => (
              <li key={idx}>{reason}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
