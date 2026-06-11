import { Routes, Route, Navigate } from 'react-router-dom';
import HomePage from '../pages/HomePage';
import MissionPage from '../pages/MissionPage';
import ReplanningPage from '../pages/ReplanningPage';
import CitiesPage from '../pages/CitiesPage';
import StadiumsPage from '../pages/StadiumsPage';
import DashboardPage from '../pages/DashboardPage';
import ProfilePage from '../pages/ProfilePage';
import MyMissionsPage from '../pages/MyMissionsPage';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/new-mission" element={<HomePage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/my-missions" element={<MyMissionsPage />} />
      <Route path="/mission/:team" element={<MissionPage />} />
      <Route path="/replan/:team" element={<ReplanningPage />} />
      <Route path="/cities" element={<CitiesPage />} />
      <Route path="/stadiums" element={<StadiumsPage />} />
      <Route
        path="*"
        element={
          <div className="page">
            <h1>404</h1>
            <p>Page not found.</p>
          </div>
        }
      />
    </Routes>
  );
}
