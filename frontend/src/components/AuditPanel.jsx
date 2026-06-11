export default function AuditPanel({ audit }) {
  if (!audit || !audit.audit || audit.audit.length === 0) {
    return (
      <div id="audit-panel" className="card">
        <h3>Audit Trail</h3>
        <p className="empty">No audit entries available.</p>
      </div>
    );
  }

  return (
    <div id="audit-panel" className="card">
      <h3>Audit Trail</h3>

      {audit.winner && (
        <p>
          <strong>Winner:</strong> {audit.winner}
        </p>
      )}

      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>City</th>
            <th>Source</th>
            <th>Final Score</th>
            <th>Top Factor</th>
            <th>Atmosphere</th>
            <th>Budget</th>
            <th>Transport</th>
          </tr>
        </thead>
        <tbody>
          {audit.audit.map((entry, idx) => (
            <tr key={idx}>
              <td>{entry.rank ?? '—'}</td>
              <td>{entry.city || '—'}</td>
              <td>{entry.candidate_source || '—'}</td>
              <td>
                {typeof entry.final_score === 'number'
                  ? entry.final_score.toFixed(2)
                  : '—'}
              </td>
              <td>{entry.reason || '—'}</td>
              <td>
                {typeof entry.audit_details?.atmosphere === 'number'
                  ? entry.audit_details.atmosphere.toFixed(2)
                  : '—'}
              </td>
              <td>
                {typeof entry.audit_details?.budget === 'number'
                  ? entry.audit_details.budget.toFixed(2)
                  : '—'}
              </td>
              <td>
                {typeof entry.audit_details?.transport === 'number'
                  ? entry.audit_details.transport.toFixed(2)
                  : '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
