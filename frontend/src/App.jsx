import { useEffect, useState } from 'react';
import { BrowserRouter, Link, NavLink } from 'react-router-dom';
import AppRoutes from './routes/AppRoutes';
import ScoutChat from './components/ScoutChat';
import { persistAccessibility, useAccessibility } from './store/useAccessibility';
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

export default function App() {
  const rawA11y = useAccessibility((state) => state.activeClasses);
  const activeA11y = Array.isArray(rawA11y) ? rawA11y : [];
  const saturation = useAccessibility((state) => state.saturation);
  const toggleClass = useAccessibility((state) => state.toggleClass);
  const setSaturation = useAccessibility((state) => state.setSaturation);
  const resetAccessibility = useAccessibility((state) => state.reset);
  const [a11yOpen, setA11yOpen] = useState(false);
  const [chatOpen, setChatOpen] = useState(false);
  const [cursorPosition, setCursorPosition] = useState({ x: -100, y: -100 });

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

  return (
    <BrowserRouter>
      <nav id="main-nav">
        <div className="nav-brand">
          <Link to="/dashboard">Scout</Link>
          <span>FIFA 2026 travel command</span>
        </div>
        <div className="nav-links">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to}>
              <span aria-hidden="true">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
          <button type="button" className="nav-ai" onClick={() => setChatOpen(true)}>
            Scout AI
          </button>
        </div>
      </nav>

      <main>
        <AppRoutes />
      </main>

      <aside className={`accessibility-panel ${a11yOpen ? 'open' : ''}`} aria-label="Accessibility settings">
        <button
          type="button"
          className="accessibility-trigger"
          aria-expanded={a11yOpen}
          onClick={() => setA11yOpen((open) => !open)}
        >
          Access
        </button>

        {a11yOpen && (
          <div className="accessibility-drawer">
            <div className="section-title">
              <h2>Accessibility Tools</h2>
              <button type="button" className="icon-btn" onClick={resetAccessibility}>
                Reset
              </button>
            </div>
            <div className="a11y-grid">
              {accessibilityOptions.map((option) => (
                <button
                  key={option.className}
                  type="button"
                  className={activeA11y.includes(option.className) ? 'active' : ''}
                  aria-pressed={activeA11y.includes(option.className)}
                  onClick={() => toggleClass(option.className)}
                >
                  <span>{option.label}</span>
                  <small>{option.group}</small>
                </button>
              ))}
            </div>
            <div className="saturation-control" aria-label="Saturation">
              <span>Saturation</span>
              {saturationModes.map((mode) => (
                <button
                  key={mode.label}
                  type="button"
                  className={saturation === mode.className ? 'active' : ''}
                  onClick={() => setSaturation(mode.className)}
                >
                  {mode.label}
                </button>
              ))}
            </div>
          </div>
        )}
      </aside>

      {activeA11y.includes('a11y-cursor') && (
        <div
          className="cursor-overlay"
          style={{ transform: `translate(${cursorPosition.x}px, ${cursorPosition.y}px)` }}
        />
      )}

      <ScoutChat open={chatOpen} onClose={() => setChatOpen((open) => !open)} />

      <nav id="bottom-nav" aria-label="Primary">
        <NavLink to="/dashboard">
          <span aria-hidden="true">D</span>
          Home
        </NavLink>
        <NavLink to="/my-missions">
          <span aria-hidden="true">M</span>
          Missions
        </NavLink>
        <button type="button" className="bottom-ai" onClick={() => setChatOpen(true)}>
          <span>AI</span>
          Scout AI
        </button>
        <NavLink to="/cities">
          <span aria-hidden="true">C</span>
          Cities
        </NavLink>
        <NavLink to="/profile">
          <span aria-hidden="true">P</span>
          Me
        </NavLink>
      </nav>
    </BrowserRouter>
  );
}
