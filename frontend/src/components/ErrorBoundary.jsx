import React from 'react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', background: 'var(--c-base)', color: 'var(--c-t1)', padding: '24px' }}>
          <h1 style={{ color: 'var(--c-red)', marginBottom: '16px' }}>Something went wrong.</h1>
          <p style={{ color: 'var(--c-t2)', marginBottom: '24px', textAlign: 'center', maxWidth: '400px' }}>
            We've encountered an unexpected error. Please try refreshing the page or restarting your session.
          </p>
          <div style={{ display: 'flex', gap: '16px' }}>
            <button className="btn" onClick={() => window.location.reload()}>Refresh Page</button>
            <button className="btn btn-secondary" onClick={() => {
              localStorage.removeItem('scout_session_v1');
              window.location.href = '/onboarding';
            }}>Reset Session</button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
