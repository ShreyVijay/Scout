import { useState } from 'react';
import { sendScoutChat } from '../services/api';

const starterPrompts = [
  'What should I watch before my next match?',
  'Find the safest replanning move.',
  'Explain my budget risk.',
];

import { Drawer } from 'vaul';

export default function ScoutChat({ open, onClose }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'I can help with mission state, routes, budget risk, and replanning decisions.',
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
        },
      });
      setMessages([
        ...nextMessages,
        { role: 'assistant', text: response.reply || 'I checked the current Scout context.' },
      ]);
    } catch (error) {
      setMessages([
        ...nextMessages,
        {
          role: 'assistant',
          text: error.response?.data?.detail || 'Scout AI is offline, but you can still use the mission and replanning tools.',
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
        aria-label="Open Scout AI"
        onClick={onClose}
      >
        AI
      </button>

      <Drawer.Root open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
        <Drawer.Portal>
          <Drawer.Overlay className="fixed inset-0 bg-black/40 z-50" style={{ background: 'rgba(0,0,0,0.6)' }} />
          <Drawer.Content className="chat-panel fixed bottom-0 left-0 right-0 z-50">
            <div className="chat-handle mx-auto w-12 h-1.5 flex-shrink-0 rounded-full bg-gray-300 mb-4" />
            <div className="section-title">
              <div>
                <p className="eyebrow">Scout AI</p>
                <h2>Travel command assistant</h2>
              </div>
              <button type="button" className="icon-btn" aria-label="Close Scout AI" onClick={onClose}>
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
                value={input}
                placeholder="Ask about routes, budget, cities..."
                onChange={(event) => setInput(event.target.value)}
              />
              <button type="submit" className="btn btn-small" disabled={loading}>
                Send
              </button>
            </form>
          </Drawer.Content>
        </Drawer.Portal>
      </Drawer.Root>
    </>
  );
}
