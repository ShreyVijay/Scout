import en from './locales/en.json';
import es from './locales/es.json';
import fr from './locales/fr.json';
import pt from './locales/pt.json';
import ar from './locales/ar.json';

const locales = { en, es, fr, pt, ar };

export function t(key, lang = 'en') {
  const parts = key.split('.');
  let node = locales[lang] || locales.en;
  for (const part of parts) node = node?.[part];
  // Fallback to English if key missing in locale
  if (node === undefined) {
    node = locales.en;
    for (const part of parts) node = node?.[part];
  }
  return node ?? key;
}
