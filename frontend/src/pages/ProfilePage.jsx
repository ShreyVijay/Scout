import { useState, useEffect } from 'react';
import { getUserProfile, updateUserProfile } from '../services/api';

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getUserProfile();
        setProfile(data);
      } catch (err) {
        setError(err.message || 'Failed to load user profile');
      } finally {
        setLoading(false);
      }
    }
    loadProfile();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    try {
      const updated = await updateUserProfile(profile);
      setProfile(updated);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err.message || 'Failed to update user profile');
    }
  }

  function handleWeightChange(field, val) {
    const floatVal = parseFloat(val);
    setProfile((prev) => ({
      ...prev,
      preferences: {
        ...prev.preferences,
        [field]: floatVal,
      },
    }));
  }

  if (loading) {
    return (
      <div id="profile-page" className="page">
        <p className="loading">Loading user profile...</p>
      </div>
    );
  }

  return (
    <div id="profile-page" className="page">
      <section className="page-header">
        <div>
          <p className="eyebrow">Preference engine</p>
          <h1>User Profile</h1>
        </div>
      </section>

      {error && <div className="error-banner">{error}</div>}
      {success && <div className="success-banner">Profile saved successfully.</div>}

      {profile && (
        <form onSubmit={handleSubmit} className="card form-panel">
          <div className="section-title">
            <h3>Profile Details</h3>
          </div>

          <label htmlFor="user-name">Full Name</label>
          <input
            id="user-name"
            type="text"
            value={profile.name || ''}
            onChange={(e) => setProfile({ ...profile, name: e.target.value })}
            required
          />

          <label htmlFor="user-email">Email Address</label>
          <input
            id="user-email"
            type="text"
            value={profile.email || ''}
            onChange={(e) => setProfile({ ...profile, email: e.target.value })}
            required
          />

          <div className="sub-section">
            <h4>Decision Intelligence Weights</h4>
            <p className="description">
              Define the default scoring weights for itinerary recommendations.
            </p>

            <div className="range-row">
              <div>
                <span>Atmosphere Weight</span>
                <span>{profile.preferences?.atmosphere_weight?.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={profile.preferences?.atmosphere_weight ?? 0.5}
                onChange={(e) => handleWeightChange('atmosphere_weight', e.target.value)}
              />
            </div>

            <div className="range-row">
              <div>
                <span>Budget Weight</span>
                <span>{profile.preferences?.budget_weight?.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={profile.preferences?.budget_weight ?? 0.3}
                onChange={(e) => handleWeightChange('budget_weight', e.target.value)}
              />
            </div>

            <div className="range-row">
              <div>
                <span>Transport Weight</span>
                <span>{profile.preferences?.transport_weight?.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={profile.preferences?.transport_weight ?? 0.2}
                onChange={(e) => handleWeightChange('transport_weight', e.target.value)}
              />
            </div>
          </div>

          <button type="submit" className="btn">Save Profile</button>
        </form>
      )}
    </div>
  );
}
