import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import HomePage from '../pages/HomePage';
import MissionPage from '../pages/MissionPage';
import ReplanningPage from '../pages/ReplanningPage';
import CitiesPage from '../pages/CitiesPage';
import StadiumsPage from '../pages/StadiumsPage';
import DashboardPage from '../pages/DashboardPage';
import ProfilePage from '../pages/ProfilePage';
import MyMissionsPage from '../pages/MyMissionsPage';
import OnboardingPage from '../pages/OnboardingPage';
import PageTransition from '../components/PageTransition';
import { useSession } from '../store/useSession';

export default function AppRoutes() {
  const location = useLocation();
  const hasOnboarded = useSession((state) => state.hasOnboarded);

  if (!hasOnboarded && location.pathname !== '/onboarding') {
    return <Navigate to="/onboarding" replace />;
  }

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/onboarding" element={<PageTransition><OnboardingPage /></PageTransition>} />


        <Route path="/dashboard" element={<PageTransition><DashboardPage /></PageTransition>} />
        <Route path="/new-mission" element={<PageTransition><HomePage /></PageTransition>} />
        <Route path="/profile" element={<PageTransition><ProfilePage /></PageTransition>} />
        <Route path="/my-missions" element={<PageTransition><MyMissionsPage /></PageTransition>} />
        <Route path="/mission/:team" element={<PageTransition><MissionPage /></PageTransition>} />
        <Route path="/replan/:team" element={<PageTransition><ReplanningPage /></PageTransition>} />
        <Route path="/cities" element={<PageTransition><CitiesPage /></PageTransition>} />
        <Route path="/stadiums" element={<PageTransition><StadiumsPage /></PageTransition>} />
        <Route
          path="*"
          element={
            <PageTransition>
              <div className="page">
                <h1>404</h1>
                <p>Page not found.</p>
              </div>
            </PageTransition>
          }
        />
      </Routes>
    </AnimatePresence>
  );
}
