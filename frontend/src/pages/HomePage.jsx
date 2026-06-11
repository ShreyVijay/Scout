import MissionForm from '../components/MissionForm';

export default function HomePage() {
  return (
    <div id="home-page" className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">New mission</p>
          <h1>skaut FIFA 2026 Travel Planner</h1>
        </div>
        <p>Create a mission to plan your team's World Cup journey.</p>
      </div>

      <MissionForm />
    </div>
  );
}
