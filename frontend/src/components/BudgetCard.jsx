function money(value) {
  return typeof value === 'number' ? `$${value.toLocaleString()}` : `$${value}`;
}

export default function BudgetCard({ mission }) {
  if (!mission) return null;

  const budget = mission.budget || {};
  const intel = mission.budget_intelligence || {};
  const totalBudget = typeof budget === 'object' ? budget.total_budget : budget;
  const estimatedCost = intel.estimated_cost ?? budget.estimated_cost ?? '-';
  const remainingBudget = intel.projected_remaining_budget ?? budget.remaining_budget ?? '-';
  const riskLevel = intel.risk_level ?? budget.risk_level ?? 'unknown';
  const spentBudget = intel.spent_budget ?? budget.spent_budget ?? 0;

  return (
    <section id="budget-card" className="card">
      <div className="section-title">
        <h3>Budget Intelligence</h3>
        <span className={`badge badge-risk-${String(riskLevel).toLowerCase()}`}>
          {riskLevel}
        </span>
      </div>

      <div className="metric-grid">
        <div className="metric-tile">
          <span>Total Budget</span>
          <strong>{money(totalBudget)}</strong>
        </div>
        <div className="metric-tile">
          <span>Spent</span>
          <strong>{money(spentBudget)}</strong>
        </div>
        <div className="metric-tile">
          <span>Remaining</span>
          <strong>{money(remainingBudget)}</strong>
        </div>
      </div>

      <p className="description">Estimated route cost: {money(estimatedCost)}</p>
    </section>
  );
}
