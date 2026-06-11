import { useSession } from '../store/useSession';

const FLAGS = {
  en: '🇺🇸',
  es: '🇪🇸',
  fr: '🇫🇷',
  pt: '🇧🇷',
  ar: '🇸🇦'
};

export default function LanguagePicker() {
  const language = useSession((state) => state.language);
  const setLanguage = useSession((state) => state.setLanguage);

  const handleSelect = (e) => {
    const newLang = e.target.value;
    setLanguage(newLang);
    if (newLang === 'ar') {
      document.documentElement.dir = 'rtl';
    } else {
      document.documentElement.dir = 'ltr';
    }
  };

  return (
    <select
      value={language}
      onChange={handleSelect}
      style={{
        padding: '6px 12px',
        borderRadius: '6px',
        backgroundColor: 'var(--c-surface)',
        color: 'var(--c-t1)',
        border: '1px solid var(--c-border)'
      }}
    >
      <option value="en">{FLAGS.en} English</option>
      <option value="es">{FLAGS.es} Español</option>
      <option value="fr">{FLAGS.fr} Français</option>
      <option value="pt">{FLAGS.pt} Português</option>
      <option value="ar">{FLAGS.ar} العربية</option>
    </select>
  );
}
