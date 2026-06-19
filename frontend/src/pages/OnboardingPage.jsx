import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useSession } from '../store/useSession';
import ThemeToggle from '../components/ThemeToggle';
import LanguagePicker from '../components/LanguagePicker'; // Need to create this
import { t } from '../i18n'; // Need to create this

export default function OnboardingPage() {
  const navigate = useNavigate();
  const session = useSession();
  
  const [step, setStep] = useState(1);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  
  const [atmosphere, setAtmosphere] = useState(50);
  const [budget, setBudget] = useState(30);
  const [transport, setTransport] = useState(20);

  const [error, setError] = useState('');

  const nextStep = () => {
    if (step === 1) {
      if (!name || !email) {
        setError('Please enter your name and email.');
        return;
      }
      if (!/^\S+@\S+\.\S+$/.test(email)) {
        setError('Please enter a valid email.');
        return;
      }
    }
    setError('');
    setStep(s => s + 1);
  };

  const completeOnboarding = async () => {
    // Optionally post to backend here
    session.setSession({
      hasOnboarded: true,
      name,
      email,
      preferences: {
        atmosphere_weight: atmosphere / 100,
        budget_weight: budget / 100,
        transport_weight: transport / 100,
      }
    });

    pendo.identify({
      visitor: {
        id: email,
        email: email,
        full_name: name,
        atmosphereWeight: atmosphere / 100,
        budgetWeight: budget / 100,
        transportWeight: transport / 100,
      }
    });

    navigate('/dashboard', { replace: true });
  };

  const variants = {
    initial: { x: 50, opacity: 0 },
    animate: { x: 0, opacity: 1 },
    exit: { x: -50, opacity: 0 },
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px',
      background: 'radial-gradient(ellipse at center, var(--c-pitch-a) 0%, var(--c-pitch-b) 100%)',
      backgroundImage: 'var(--pitch)'
    }}>
      <div className="card" style={{ maxWidth: '480px', width: '100%', overflow: 'hidden', position: 'relative', minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', marginBottom: '24px' }}>
          {[1, 2, 3].map(i => (
            <div key={i} style={{
              width: '8px', height: '8px', borderRadius: '50%',
              backgroundColor: i === step ? 'var(--c-amber)' : 'var(--c-border)'
            }} />
          ))}
        </div>

        <div style={{ flex: 1, position: 'relative' }}>
          <AnimatePresence mode="wait">
            {step === 1 && (
              <motion.div key="step1" variants={variants} initial="initial" animate="animate" exit="exit" transition={{ duration: 0.2 }}>
                <h2>Who are you following?</h2>
                <p style={{ color: 'var(--c-t2)', marginBottom: '24px' }}>Let's get your skaut profile set up.</p>
                
                {error && <div className="error-banner" style={{ marginBottom: '16px', color: 'var(--c-red)' }}>{error}</div>}
                
                <label>Your name</label>
                <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="e.g. Alex" style={{ width: '100%', marginBottom: '16px' }} />
                
                <label>Email address</label>
                <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="alex@example.com" style={{ width: '100%', marginBottom: '24px' }} />
                
                <button onClick={nextStep} style={{ width: '100%' }}>Continue</button>
              </motion.div>
            )}

            {step === 2 && (
              <motion.div key="step2" variants={variants} initial="initial" animate="animate" exit="exit" transition={{ duration: 0.2 }}>
                <h2>Language & Theme</h2>
                <p style={{ color: 'var(--c-t2)', marginBottom: '24px' }}>Customize your skaut experience.</p>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', padding: '16px', border: '1px solid var(--c-border)', borderRadius: '8px' }}>
                  <span>Language</span>
                  <LanguagePicker />
                </div>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px', padding: '16px', border: '1px solid var(--c-border)', borderRadius: '8px' }}>
                  <span>Theme</span>
                  <ThemeToggle />
                </div>
                
                <div style={{ display: 'flex', gap: '12px' }}>
                  <button className="secondary" onClick={() => setStep(1)} style={{ flex: 1 }}>Back</button>
                  <button onClick={nextStep} style={{ flex: 2 }}>Continue</button>
                </div>
              </motion.div>
            )}

            {step === 3 && (
              <motion.div key="step3" variants={variants} initial="initial" animate="animate" exit="exit" transition={{ duration: 0.2 }}>
                <h2>Travel Preferences</h2>
                <p style={{ color: 'var(--c-t2)', marginBottom: '24px' }}>How do you prioritize your trips?</p>
                
                <label style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Atmosphere</span>
                  <span>{atmosphere}%</span>
                </label>
                <input type="range" min="0" max="100" value={atmosphere} onChange={e => setAtmosphere(parseInt(e.target.value))} style={{ width: '100%', marginBottom: '16px', '--val': atmosphere }} />
                
                <label style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Budget</span>
                  <span>{budget}%</span>
                </label>
                <input type="range" min="0" max="100" value={budget} onChange={e => setBudget(parseInt(e.target.value))} style={{ width: '100%', marginBottom: '16px', '--val': budget }} />
                
                <label style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>Transport</span>
                  <span>{transport}%</span>
                </label>
                <input type="range" min="0" max="100" value={transport} onChange={e => setTransport(parseInt(e.target.value))} style={{ width: '100%', marginBottom: '32px', '--val': transport }} />
                
                <div style={{ display: 'flex', gap: '12px' }}>
                  <button className="secondary" onClick={() => setStep(2)} style={{ flex: 1 }}>Back</button>
                  <button onClick={completeOnboarding} style={{ flex: 2 }}>Complete</button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
