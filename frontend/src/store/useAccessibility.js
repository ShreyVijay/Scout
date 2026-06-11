import { create } from 'zustand';

const STORAGE_KEY = 'scout_accessibility';
const SATURATION_KEY = 'scout_saturation';

function readClasses() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export const useAccessibility = create((set) => ({
  activeClasses: readClasses(),
  saturation: localStorage.getItem(SATURATION_KEY) || '',
  toggleClass: (className) =>
    set((state) => ({
      activeClasses: state.activeClasses.includes(className)
        ? state.activeClasses.filter((item) => item !== className)
        : [...state.activeClasses, className],
    })),
  setSaturation: (className) => set({ saturation: className }),
  reset: () => set({ activeClasses: [], saturation: '' }),
}));

export function persistAccessibility(activeClasses, saturation) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(activeClasses));
  localStorage.setItem(SATURATION_KEY, saturation);
}
