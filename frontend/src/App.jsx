import { useEffect, useState } from 'react';
import { BrowserRouter, Link, NavLink, useLocation } from 'react-router-dom';
import AppRoutes from './routes/AppRoutes';
import ScoutChat from './components/ScoutChat';
import skautLogo from './assets/skaut-logo.png';
import { persistAccessibility, useAccessibility } from './store/useAccessibility';
import { useSession } from './store/useSession';
import ThemeToggle from './components/ThemeToggle';
import ErrorBoundary from './components/ErrorBoundary';
import { Toaster, toast } from 'sonner';
import { t } from './i18n';
import './styles.css';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: 'D' },
  { to: '/my-missions', label: 'Missions', icon: 'M' },
  { to: '/cities', label: 'Cities', icon: 'C' },
  { to: '/stadiums', label: 'Stadiums', icon: 'S' },
  { to: '/profile', label: 'Profile', icon: 'P' },
];

const accessibilityOptions = [
  { className: 'a11y-bigger-text', label: 'Bigger Text', group: 'Reading' },
  { className: 'a11y-text-spacing', label: 'Text Spacing', group: 'Reading' },
  { className: 'a11y-line-height', label: 'Line Height', group: 'Reading' },
  { className: 'a11y-text-align', label: 'Left Align', group: 'Reading' },
  { className: 'a11y-pause-animations', label: 'Pause Motion', group: 'Motion' },
  { className: 'a11y-hide-images', label: 'Hide Images', group: 'Visual' },
  { className: 'a11y-highlight-links', label: 'Highlight Links', group: 'Visual' },
  { className: 'a11y-contrast', label: 'Contrast+', group: 'Visual' },
  { className: 'a11y-cursor', label: 'Large Cursor', group: 'Visual' },
  { className: 'a11y-dyslexia', label: 'Dyslexia Font', group: 'Reading' },
  { className: 'a11y-structure', label: 'Page Structure', group: 'Structure' },
];

const saturationModes = [
  { className: '', label: 'Normal' },
  { className: 'a11y-sat-low', label: 'Low' },
  { className: 'a11y-sat-off', label: 'Off' },
  { className: 'a11y-sat-high', label: 'High' },
];

function AppLayout() {
  const rawA11y = useAccessibility((state) => state.activeClasses);
  const activeA11y = Array.isArray(rawA11y) ? rawA11y : [];
  const saturation = useAccessibility((state) => state.saturation);
  const theme = useSession((state) => state.theme);
  const language = useSession((state) => state.language);

  const [chatOpen, setChatOpen] = useState(false);
  const [cursorPosition, setCursorPosition] = useState({ x: -100, y: -100 });
  const location = useLocation();

  const isMapRoute = ['/mission/', '/replan/', '/cities'].some(r => location.pathname.startsWith(r));
  const isOnboarding = location.pathname === '/onboarding';

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  useEffect(() => {
    const root = document.documentElement;
    const allClasses = [
      ...accessibilityOptions.map((option) => option.className),
      ...saturationModes.map((mode) => mode.className).filter(Boolean),
      'a11y-large-text',
      'a11y-reduced-motion',
    ];

    allClasses.forEach((className) => root.classList.remove(className));
    activeA11y.forEach((className) => root.classList.add(className));
    if (saturation) root.classList.add(saturation);

    persistAccessibility(activeA11y, saturation);
  }, [activeA11y, saturation]);

  useEffect(() => {
    if (!activeA11y.includes('a11y-cursor')) return undefined;

    function handleMove(event) {
      setCursorPosition({ x: event.clientX, y: event.clientY });
    }

    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, [activeA11y]);

  useEffect(() => {
    if (isOnboarding) return;
    
    const messages = [
      "Checking flight prices for Dallas...",
      "Monitoring hotel availability in Los Angeles...",
      "Analyzing Group Stage ticket drops...",
      "Scanning route optimizations for Mexico City...",
      "Updating local weather forecasts for Seattle...",
      "Recalculating budget risk based on current spending...",
      "Syncing tournament schedule updates..."
    ];

    const interval = setInterval(() => {
      const msg = messages[Math.floor(Math.random() * messages.length)];
      toast(msg, {
        description: "skaut AI is running in the background",
        duration: 4000,
        position: "bottom-left"
      });
    }, 20000);

    return () => clearInterval(interval);
  }, [isOnboarding]);

  return (
    <>
      <Toaster richColors position="top-right" />
      {!isOnboarding && (
        <nav id="main-nav">
          <div className="nav-brand">
            <Link to="/dashboard" className="brand-lockup" aria-label="skaut dashboard">
              <img src={skautLogo} alt="" />
              <span>skaut</span>
            </Link>
            {isMapRoute && <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: 'var(--c-green)', marginLeft: 8 }} />}
            <span>FIFA 2026 travel command</span>
          </div>
          <div className="nav-links">
            {navItems.map((item) => (
              <NavLink key={item.to} to={item.to}>
                <span aria-hidden="true">{item.icon}</span>
                {t(`nav.${item.label.toLowerCase()}`, language)}
              </NavLink>
            ))}
            <ThemeToggle />
            <button type="button" className="nav-ai" onClick={() => setChatOpen(true)}>
              {t('nav.scout', language)}
            </button>
          </div>
        </nav>
      )}

      <main>
        <AppRoutes />
      </main>

      {activeA11y.includes('a11y-cursor') && (
        <div
          className="cursor-overlay"
          style={{ transform: `translate(${cursorPosition.x}px, ${cursorPosition.y}px)` }}
        />
      )}

      {!isOnboarding && (
        <ScoutChat
          open={chatOpen}
          onOpen={() => setChatOpen(true)}
          onClose={() => setChatOpen(false)}
        />
      )}

      {!isOnboarding && (
        <nav id="bottom-nav" aria-label="Primary">
          <NavLink to="/dashboard">
            <span aria-hidden="true">D</span>
            {t('nav.dashboard', language)}
          </NavLink>
          <NavLink to="/my-missions">
            <span aria-hidden="true">M</span>
            {t('nav.missions', language)}
          </NavLink>
          <button type="button" className="bottom-ai" onClick={() => setChatOpen(true)}>
            <span>⚡</span>
            {t('nav.scout', language)}
          </button>
          <NavLink to="/cities">
            <span aria-hidden="true">C</span>
            {t('nav.cities', language)}
          </NavLink>
          <NavLink to="/profile">
            <span aria-hidden="true">P</span>
            {t('nav.profile', language)}
          </NavLink>
        </nav>
      )}
    </>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AppLayout />
      </BrowserRouter>
    </ErrorBoundary>
  );
}
