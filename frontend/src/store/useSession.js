import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const initialState = {
  hasOnboarded: false,
  name: '',
  email: '',
  language: 'en',
  theme: 'dark',
  preferences: {
    atmosphere_weight: 0.5,
    budget_weight: 0.3,
    transport_weight: 0.2,
  },
  accessibility: {
    activeClasses: [],
    saturation: '',
  },
};

export const useSession = create(
  persist(
    (set) => ({
      ...initialState,
      setSession: (data) => set((state) => ({ ...state, ...data })),
      updatePreferences: (prefs) => set((state) => ({ preferences: { ...state.preferences, ...prefs } })),
      setTheme: (theme) => set({ theme }),
      setLanguage: (language) => set({ language }),
      setAccessibility: (updater) => set((state) => {
        const nextA11y = typeof updater === 'function' ? updater(state.accessibility) : updater;
        return { accessibility: { ...state.accessibility, ...nextA11y } };
      }),
      reset: () => set(initialState),
    }),
    {
      name: 'scout_session_v1',
    }
  )
);
