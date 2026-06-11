import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createMission } from '../services/api';
import { useSession } from '../store/useSession';

export default function MissionForm() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    team: '',
    budget: '',
    travel_style: 'budget',
    objective: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const email = useSession.getState().email;
      const payload = {
        ...form,
        budget: parseInt(form.budget, 10),
        email: email
      };

      const result = await createMission(payload);
      const team = result.team || form.team;
      navigate(`/mission/${encodeURIComponent(team)}`);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to create mission'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <form id="mission-form" className="card" onSubmit={handleSubmit}>
      <h2>Create Mission</h2>

      {error && <div className="error-banner">{error}</div>}

      <label htmlFor="field-team">Team</label>
      <input
        id="field-team"
        name="team"
        type="text"
        placeholder="e.g. Egypt"
        value={form.team}
        onChange={handleChange}
        required
      />

      <label htmlFor="field-budget">Budget ($)</label>
      <input
        id="field-budget"
        name="budget"
        type="number"
        placeholder="e.g. 5000"
        value={form.budget}
        onChange={handleChange}
        required
        min="0"
      />

      <label htmlFor="field-travel-style">Travel Style</label>
      <select
        id="field-travel-style"
        name="travel_style"
        value={form.travel_style}
        onChange={handleChange}
      >
        <option value="budget">Budget</option>
        <option value="comfort">Comfort</option>
        <option value="luxury">Luxury</option>
      </select>

      <label htmlFor="field-objective">Objective</label>
      <textarea
        id="field-objective"
        name="objective"
        placeholder="e.g. Follow the team to the final"
        value={form.objective}
        onChange={handleChange}
        required
        rows={3}
      />

      <button
        id="btn-create-mission"
        type="submit"
        disabled={loading}
      >
        {loading ? 'Creating...' : 'Create Mission'}
      </button>
    </form>
  );
}
