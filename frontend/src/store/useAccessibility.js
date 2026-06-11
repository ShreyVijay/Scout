import { useSession } from './useSession';

export const useAccessibility = (selector) => {
  const accessibility = useSession((state) => state.accessibility);
  const setAccessibility = useSession((state) => state.setAccessibility);

  const api = {
    activeClasses: accessibility.activeClasses || [],
    saturation: accessibility.saturation || '',
    toggleClass: (className) =>
      setAccessibility((a11y) => ({
        activeClasses: a11y.activeClasses.includes(className)
          ? a11y.activeClasses.filter((item) => item !== className)
          : [...a11y.activeClasses, className],
      })),
    setSaturation: (className) => setAccessibility({ saturation: className }),
    reset: () => setAccessibility({ activeClasses: [], saturation: '' }),
  };

  return selector(api);
};

export function persistAccessibility() {
  // Now handled by zustand/middleware persist in useSession
}
