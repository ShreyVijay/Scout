import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useWallet = create(
  persist(
    (set) => ({
      balance: 5000,
      transactions: [
        { id: 1, type: 'deposit', amount: 5000, date: new Date().toISOString(), note: 'Initial funding' }
      ],
      addFunds: (amount) => set((state) => ({
        balance: state.balance + amount,
        transactions: [
          { id: Date.now(), type: 'deposit', amount, date: new Date().toISOString(), note: 'Added funds' },
          ...state.transactions
        ]
      })),
      spendFunds: (amount, note) => set((state) => ({
        balance: state.balance - amount,
        transactions: [
          { id: Date.now(), type: 'withdrawal', amount, date: new Date().toISOString(), note },
          ...state.transactions
        ]
      }))
    }),
    {
      name: 'scout_wallet_v1'
    }
  )
);
