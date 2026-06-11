import { useEffect, useState } from 'react';
import { BrowserRouter, Link, NavLink } from 'react-router-dom';
import AppRoutes from './routes/AppRoutes';
import './styles.css';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: '⌂' },
  { to: '/my-missions', label: 'Missions', icon: '◎' },
  { to: '/new-mission', label: 'Create', icon: '+' },
  { to: '/cities', label: 'Cities', icon: '◆' },
  { to: '/stadiums', label: 'Stadiums', icon: '▣' },
];

const accessibilityOptions = [
  { key: 'contrast', label: 'Contrast+' },
  { key: 'largeText', label: 'Large text' },
  { key: 'reducedMotion', label: 'Calm motion' },
];

export default function App() {
  const [accessibility, setAccessibility] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('scout_accessibility') || '{}');
    } catch {
      return {};
    }
  });

  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle('a11y-contrast', Boolean(accessibility.contrast));
    root.classList.toggle('a11y-large-text', Boolean(accessibility.largeText));
    root.classList.toggle('a11y-reduced-motion', Boolean(accessibility.reducedMotion));
    localStorage.setItem('scout_accessibility', JSON.stringify(accessibility));
  }, [accessibility]);

  function toggleAccessibility(key) {
    setAccessibility((current) => ({
      ...current,
      [key]: !current[key],
    }));
  }

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
          <NavLink to="/profile">
            <span aria-hidden="true">◌</span>
            Profile
          </NavLink>
        </div>
      </nav>

      <main>
        <AppRoutes />
      </main>

      <aside className="accessibility-panel" aria-label="Accessibility settings">
        {accessibilityOptions.map((option) => (
          <button
            key={option.key}
            type="button"
            className={accessibility[option.key] ? 'active' : ''}
            aria-pressed={Boolean(accessibility[option.key])}
            onClick={() => toggleAccessibility(option.key)}
          >
            {option.label}
          </button>
        ))}
      </aside>

      <nav id="bottom-nav" aria-label="Primary">
        {navItems.slice(0, 4).map((item) => (
          <NavLink key={item.to} to={item.to}>
            <span aria-hidden="true">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>
    </BrowserRouter>
  );
}
