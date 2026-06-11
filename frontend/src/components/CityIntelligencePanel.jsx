export default function CityIntelligencePanel({ city }) {
  if (!city) return null;

  return (
    <div id="city-intelligence-panel" className="card">
      <h3>{city.city || 'City Details'}</h3>

      <table>
        <tbody>
          <tr>
            <td className="label">Country</td>
            <td>{city.country || '—'}</td>
          </tr>
          <tr>
            <td className="label">Atmosphere Score</td>
            <td>{city.atmosphere_score ?? '—'}</td>
          </tr>
          <tr>
            <td className="label">Budget Score</td>
            <td>{city.budget_score ?? '—'}</td>
          </tr>
          <tr>
            <td className="label">Transport Score</td>
            <td>{city.transport_score ?? '—'}</td>
          </tr>
          <tr>
            <td className="label">Fan Zone Score</td>
            <td>{city.fan_zone_score ?? '—'}</td>
          </tr>
        </tbody>
      </table>

      {city.description && (
        <p className="description">{city.description}</p>
      )}

      {city.stadiums && city.stadiums.length > 0 && (
        <div className="sub-section">
          <h4>Stadiums</h4>
          <table>
            <thead>
              <tr>
                <th>Stadium</th>
                <th>Capacity</th>
              </tr>
            </thead>
            <tbody>
              {city.stadiums.map((s, idx) => (
                <tr key={idx}>
                  <td>{s.stadium || '—'}</td>
                  <td>{s.capacity ? s.capacity.toLocaleString() : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
