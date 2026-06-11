import { useEffect } from 'react';

export default function GoalOverlay({ visible, scorer = 'skaut route update', onDismiss }) {
  useEffect(() => {
    if (!visible) return undefined;
    const timer = window.setTimeout(onDismiss, 3200);
    return () => window.clearTimeout(timer);
  }, [visible, onDismiss]);

  if (!visible) return null;

  return (
    <button type="button" className="goal-overlay" onClick={onDismiss}>
      <span className="goal-ball" aria-hidden="true" />
      <span className="goal-word">GOAAAL!</span>
      <span className="goal-scorer">{scorer}</span>
      <span className="goal-help">Tap to dismiss</span>
      <span className="confetti c1" aria-hidden="true" />
      <span className="confetti c2" aria-hidden="true" />
      <span className="confetti c3" aria-hidden="true" />
      <span className="confetti c4" aria-hidden="true" />
      <span className="confetti c5" aria-hidden="true" />
    </button>
  );
}
