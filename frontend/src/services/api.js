import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      // Clear local storage session
      localStorage.removeItem('scout_session_v1');
      window.location.href = '/onboarding';
    }
    return Promise.reject(error);
  }
);

// ── Mission ────────────────────────────────────────────────────

export async function createMission(data) {
  const response = await api.post('/mission', data);
  return response.data;
}

export async function getMission(team) {
  const response = await api.get(`/mission/${encodeURIComponent(team)}`);
  return response.data;
}

// ── Replanning ─────────────────────────────────────────────────

export async function runReplanning(team) {
  const response = await api.post(`/replan/${encodeURIComponent(team)}`);
  return response.data;
}

// ── Cities ─────────────────────────────────────────────────────

export async function getCities() {
  const response = await api.get('/cities');
  return response.data;
}

export async function getCityDetail(city) {
  const response = await api.get(`/city/${encodeURIComponent(city)}`);
  return response.data;
}

// ── Stadiums ───────────────────────────────────────────────────

export async function getStadiums() {
  const response = await api.get('/stadiums');
  return response.data;
}

export async function getStadiumDetail(stadium) {
  const response = await api.get(`/stadium/${encodeURIComponent(stadium)}`);
  return response.data;
}

// ── Budget ─────────────────────────────────────────────────────

export async function getBudgetStatus(team) {
  const response = await api.get(`/budget/${encodeURIComponent(team)}`);
  return response.data;
}

// ── Preferences ────────────────────────────────────────────────

export async function getPreferences(team) {
  const response = await api.get(`/preferences/${encodeURIComponent(team)}`);
  return response.data;
}

// ── User Profile ───────────────────────────────────────────────

export async function getUserProfile() {
  const response = await api.get('/user');
  return response.data;
}

export async function updateUserProfile(data) {
  const response = await api.post('/user', data);
  return response.data;
}

export async function getMissions(email) {
  const response = await api.get('/missions', { params: { email } });
  return response.data;
}

export async function sendScoutChat(data) {
  const response = await api.post('/chat', data);
  return response.data;
}

// ── Travel Intelligence ────────────────────────────────────────

export async function getTravelFlights(origin, destination, departureDate) {
  const response = await api.get('/travel/flights', {
    params: { origin, destination, departure_date: departureDate }
  });
  return response.data;
}

export async function getTravelHotels(city) {
  const response = await api.get('/travel/hotels', {
    params: { city }
  });
  return response.data;
}

export async function getTravelBuses(origin, destination, departureDate) {
  const response = await api.get('/travel/buses', {
    params: { origin, destination, departure_date: departureDate }
  });
  return response.data;
}

export async function getTravelTickets(match) {
  const response = await api.get('/travel/tickets', {
    params: { match }
  });
  return response.data;
}

export default api;
