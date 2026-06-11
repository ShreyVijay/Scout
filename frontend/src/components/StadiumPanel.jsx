export default function StadiumPanel({ stadium }) {
  if (!stadium) return null;

  return (
    <div id="stadium-panel" className="card">
      <h3>{stadium.stadium || 'Stadium Details'}</h3>
      <table>
        <tbody>
          <tr>
            <td className="label">City</td>
            <td>{stadium.city || '—'}</td>
          </tr>
          <tr>
            <td className="label">Capacity</td>
            <td>{stadium.capacity ? stadium.capacity.toLocaleString() : '—'}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}
