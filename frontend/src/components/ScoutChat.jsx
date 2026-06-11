import { useState } from 'react';
import { Drawer } from 'vaul';
import { sendScoutChat } from '../services/api';
import { useSession } from '../store/useSession';
import { t } from '../i18n';

export default function ScoutChat({ open, onOpen, onClose }) {
  const language = useSession((state) => state.language);
  const name = useSession((state) => state.name);

  const starterPrompts = [
    t('chat.prompt_watch', language) || 'What should I watch before my next match?',
    t('chat.prompt_safe', language) || 'Find the safest replanning move.',
    t('chat.prompt_risk', language) || 'Explain my budget risk.',
  ];

  const greeting = t('chat.greeting', language).replace('{name}', name || 'Traveler');

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: greeting,
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  async function sendMessage(text = input) {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    const nextMessages = [...messages, { role: 'user', text: trimmed }];
    setMessages(nextMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await sendScoutChat({
        message: trimmed,
        context: {
          surface: window.location.pathname,
          saved_recommendations: JSON.parse(localStorage.getItem('saved_recommendations') || '[]'),
          language: language,
          user_name: name,
        },
      });
      setMessages([
        ...nextMessages,
        { role: 'assistant', text: response.reply || 'I checked the current skaut context.' },
      ]);
    } catch (error) {
      setMessages([
        ...nextMessages,
        {
          role: 'assistant',
          text: error.response?.data?.detail || 'skaut AI is offline, but you can still use the mission and replanning tools.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <button
        type="button"
        className="chat-fab"
        aria-label="Open skaut AI"
        onClick={onOpen}
      >
        AI
      </button>

      <Drawer.Root open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
        <Drawer.Portal>
          <Drawer.Overlay className="fixed inset-0 bg-black/40 z-50" style={{ background: 'rgba(0,0,0,0.6)' }} />
          <Drawer.Content className="chat-panel fixed bottom-0 left-0 right-0 z-50">
            <Drawer.Title className="sr-only">skaut travel command assistant</Drawer.Title>
            <Drawer.Description className="sr-only">
              Ask skaut about FIFA 2026 routes, cities, stadiums, budgets, and replanning.
            </Drawer.Description>
            <div className="chat-handle mx-auto w-12 h-1.5 flex-shrink-0 rounded-full bg-gray-300 mb-4" />
            <div className="section-title">
              <div>
                <p className="eyebrow">{t('nav.scout', language)}</p>
                <h2>Travel command assistant</h2>
              </div>
              <button type="button" className="icon-btn" aria-label="Close skaut AI" onClick={onClose}>
                X
              </button>
            </div>

            <div className="chat-prompts">
              {starterPrompts.map((prompt) => (
                <button key={prompt} type="button" onClick={() => sendMessage(prompt)}>
                  {prompt}
                </button>
              ))}
            </div>

            <div className="chat-log">
              {messages.map((message, index) => (
                <div key={index} className={`chat-message ${message.role}`}>
                  {message.text}
                </div>
              ))}
              {loading && <div className="chat-message assistant">Thinking through the route...</div>}
            </div>

            <form
              className="chat-compose"
              onSubmit={(event) => {
                event.preventDefault();
                sendMessage();
              }}
            >
              <input
                type="text"
                placeholder={t('chat.placeholder', language)}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={loading}
              />
              <button type="submit" disabled={!input.trim() || loading}>
                Send
              </button>
            </form>
          </Drawer.Content>
        </Drawer.Portal>
      </Drawer.Root>
    </>
  );
}
