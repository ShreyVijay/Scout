import { useState } from 'react';
import { Drawer } from 'vaul';
import { useWallet } from '../store/useWallet';
import { useSession } from '../store/useSession';
import { t } from '../i18n';

export default function WalletDrawer({ open, onClose }) {
  const language = useSession((state) => state.language);
  const { balance, transactions, addFunds } = useWallet();
  const [amount, setAmount] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  const handleAdd = (e) => {
    e.preventDefault();
    const val = parseFloat(amount);
    if (!isNaN(val) && val > 0) {
      addFunds(val);
      setAmount('');
      setIsAdding(false);
    }
  };

  return (
    <Drawer.Root open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 bg-black/40 z-50" style={{ background: 'rgba(0,0,0,0.6)' }} />
        <Drawer.Content className="fixed bottom-0 left-0 right-0 z-50" style={{ 
          background: 'var(--c-base)', 
          borderTopLeftRadius: '20px', 
          borderTopRightRadius: '20px',
          maxHeight: '85vh',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <div className="chat-handle mx-auto w-12 h-1.5 flex-shrink-0 rounded-full bg-gray-300 mb-4" style={{ margin: '12px auto', background: 'var(--c-border)' }} />
          <div className="section-title" style={{ padding: '0 24px' }}>
            <div>
              <p className="eyebrow">Financials</p>
              <h2>{t('wallet.title', language)}</h2>
            </div>
            <button type="button" className="icon-btn" aria-label="Close" onClick={onClose}>
              X
            </button>
          </div>

          <div style={{ padding: '24px', flex: 1, overflowY: 'auto' }}>
            <div className="card" style={{ background: 'linear-gradient(135deg, var(--c-surface), var(--c-card))', border: '1px solid var(--c-border)', marginBottom: '24px' }}>
              <p style={{ color: 'var(--c-t2)', fontSize: '0.9rem', marginBottom: '8px' }}>{t('wallet.balance', language)}</p>
              <h1 style={{ fontSize: '2.5rem', color: 'var(--c-t1)', margin: 0 }}>
                ${balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}
              </h1>
              <div style={{ marginTop: '24px' }}>
                {!isAdding ? (
                  <button className="btn" onClick={() => setIsAdding(true)} style={{ width: '100%' }}>
                    {t('wallet.add_funds', language)}
                  </button>
                ) : (
                  <form onSubmit={handleAdd} style={{ display: 'flex', gap: '8px' }}>
                    <input 
                      type="number" 
                      placeholder="Amount" 
                      value={amount}
                      onChange={e => setAmount(e.target.value)}
                      style={{ flex: 1, padding: '12px', borderRadius: '8px', border: '1px solid var(--c-border)', background: 'var(--c-surface)', color: 'white' }}
                      autoFocus
                    />
                    <button type="submit" className="btn">Add</button>
                    <button type="button" className="btn btn-secondary" onClick={() => setIsAdding(false)}>Cancel</button>
                  </form>
                )}
              </div>
            </div>

            <h3 style={{ marginBottom: '16px', fontSize: '1.1rem' }}>Recent Activity</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {transactions.map(tx => (
                <div key={tx.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px', background: 'var(--c-surface)', borderRadius: '8px' }}>
                  <div>
                    <strong style={{ display: 'block', color: 'var(--c-t1)' }}>{tx.note}</strong>
                    <span style={{ fontSize: '0.8rem', color: 'var(--c-t3)' }}>{new Date(tx.date).toLocaleDateString()}</span>
                  </div>
                  <strong style={{ color: tx.type === 'deposit' ? 'var(--c-green)' : 'var(--c-t1)' }}>
                    {tx.type === 'deposit' ? '+' : '-'}${tx.amount.toLocaleString()}
                  </strong>
                </div>
              ))}
            </div>
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}
