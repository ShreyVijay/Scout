import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSession } from '../store/useSession';
import { useWallet } from '../store/useWallet';
import { t } from '../i18n';
import LanguagePicker from '../components/LanguagePicker';
import ThemeToggle from '../components/ThemeToggle';
import WalletDrawer from '../components/WalletDrawer';

export default function ProfilePage() {
  const session = useSession();
  const balance = useWallet((state) => state.balance);
  const navigate = useNavigate();
  const [walletOpen, setWalletOpen] = useState(false);

  const handleClearSession = () => {
    if (window.confirm('Are you sure you want to clear your local session and restart onboarding?')) {
      session.clearSession();
      navigate('/onboarding', { replace: true });
    }
  };

  return (
    <div id="profile-page" className="page">
      <section className="page-header">
        <div>
          <p className="eyebrow">{t('nav.profile', session.language) || 'Profile'}</p>
          <h1>{session.name || 'Traveler'}</h1>
          <p style={{ color: 'var(--c-t2)', marginTop: '4px' }}>{session.email}</p>
        </div>
      </section>

      <div className="grid-2" style={{ gap: '24px' }}>
        <section className="card">
          <div className="section-title">
            <h3>App Settings</h3>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>Language</strong>
                <p style={{ fontSize: '0.8rem', color: 'var(--c-t2)', margin: 0 }}>Select your preferred language</p>
              </div>
              <LanguagePicker />
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>Theme</strong>
                <p style={{ fontSize: '0.8rem', color: 'var(--c-t2)', margin: 0 }}>Toggle light/dark mode</p>
              </div>
              <ThemeToggle />
            </div>
          </div>
        </section>

        <section className="card">
          <div className="section-title">
            <h3>Financials</h3>
          </div>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
            <div>
              <strong>Wallet Balance</strong>
              <p style={{ fontSize: '0.8rem', color: 'var(--c-t2)', margin: 0 }}>Current available funds</p>
            </div>
            <strong style={{ fontSize: '1.25rem', color: 'var(--c-amber)' }}>
              ${balance.toLocaleString()}
            </strong>
          </div>
          
          <button className="btn" onClick={() => setWalletOpen(true)} style={{ width: '100%' }}>
            Manage Wallet
          </button>
        </section>

        <section className="card">
          <div className="section-title">
            <h3>Travel Preferences</h3>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <div style={{ fontSize: '0.8rem', color: 'var(--c-t2)' }}>Travel Style</div>
              <strong style={{ textTransform: 'capitalize' }}>{session.travelStyle || 'Balanced'}</strong>
            </div>
            <div>
              <div style={{ fontSize: '0.8rem', color: 'var(--c-t2)' }}>Default Budget Limit</div>
              <strong>${session.budgetLimit || 5000}</strong>
            </div>
          </div>
        </section>

        <section className="card" style={{ border: '1px solid var(--c-red)' }}>
          <div className="section-title">
            <h3 style={{ color: 'var(--c-red)' }}>Danger Zone</h3>
          </div>
          <p style={{ fontSize: '0.9rem', color: 'var(--c-t2)', marginBottom: '16px' }}>
            Clear your local session data. This will not delete backend missions, but will reset your onboarding state.
          </p>
          <button className="btn" style={{ background: 'var(--c-red)', color: 'white' }} onClick={handleClearSession}>
            Clear Session & Restart
          </button>
        </section>
      </div>

      <WalletDrawer open={walletOpen} onClose={() => setWalletOpen(false)} />
    </div>
  );
}
