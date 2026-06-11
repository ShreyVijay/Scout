import { useSession } from '../store/useSession';
import { Sun, Moon } from '@phosphor-icons/react';

export default function ThemeToggle() {
  const theme = useSession((state) => state.theme);
  const setTheme = useSession((state) => state.setTheme);

  const isLight = theme === 'light';

  return (
    <button
      type="button"
      className="icon-btn"
      aria-label="Toggle Theme"
      onClick={() => setTheme(isLight ? 'dark' : 'light')}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'transparent',
        border: 'none',
        color: 'var(--c-t2)',
        cursor: 'pointer',
        padding: '8px'
      }}
    >
      {isLight ? <Moon size={20} weight="bold" /> : <Sun size={20} weight="bold" />}
    </button>
  );
}
