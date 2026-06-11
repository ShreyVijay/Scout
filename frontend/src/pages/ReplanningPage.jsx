import { useState, useEffect } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  runReplanning,
  getMission,
  getTravelFlights,
  getTravelHotels,
  getTravelBuses,
  getTravelTickets,
} from '../services/api';
import { searchHotels, searchFood } from '../services/placesService';
import MapView from '../components/map/MapView';
import HotelMap from '../components/map/HotelMap';
import FoodMap from '../components/map/FoodMap';
import DirectionsRoute from '../components/map/DirectionsRoute';
import RecommendationCard from '../components/RecommendationCard';
import RankingTable from '../components/RankingTable';
import ReasoningPanel from '../components/ReasoningPanel';
import AuditPanel from '../components/AuditPanel';
import { HeroReplanning } from '../components/PitchUI';

function OptionsTable({ title, empty, items, priceLabel = 'Price' }) {
  return (
    <div className="sub-section">
      <h4>{title}</h4>
      {items.length === 0 ? (
        <p className="empty">{empty}</p>
      ) : (
        <div className="data-grid">
          {items.map((item, index) => (
            <article key={`${item.provider}-${index}`} className="data-card">
              <strong>{item.provider || 'Provider'}</strong>
              <span>{priceLabel}: {item.price || item.rate || '-'}</span>
              <p className="description">Availability: {item.availability || '-'}</p>
            </article>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ReplanningPage() {
  const { team } = useParams();
  const [mission, setMission] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showHotels, setShowHotels] = useState(true);
  const [showFood, setShowFood] = useState(true);
  const [showRoute, setShowRoute] = useState(true);
  const [hotelsList, setHotelsList] = useState([]);
  const [foodList, setFoodList] = useState([]);
  const [travelOptions, setTravelOptions] = useState({
    flights: [],
    hotels: [],
    buses: [],
    tickets: [],
  });
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    async function loadMission() {
      try {
        const data = await getMission(team);
        setMission(data);
      } catch (err) {
        console.error('Failed to load mission details for routing context:', err);
      }
    }

    loadMission();
  }, [team]);

  async function handleReplan() {
    setLoading(true);
    setError(null);
    setResult(null);
    setSavedSuccess(false);

    try {
      const data = await runReplanning(team);
      setResult(data);

      const recCity = data.recommendation?.city;
      const matchName = data.recommendation?.match || 'World Cup Match';
      const startCity = mission?.itinerary?.[mission.itinerary.length - 1]?.city || 'Miami';

      if (recCity) {
        // Mock lat/lng for Places Service just to trigger search
        const lat = 25.7617, lng = -80.1918;
        const hotels = await searchHotels(recCity, lat, lng);
        const food = await searchFood(recCity, lat, lng);
        setHotelsList(hotels);
        setFoodList(food);

        const flightRes = await getTravelFlights(startCity, recCity);
        const hotelRes = await getTravelHotels(recCity);
        const busRes = await getTravelBuses(startCity, recCity);
        const ticketRes = await getTravelTickets(matchName);

        setTravelOptions({
          flights: flightRes.flights || [],
          hotels: hotelRes.hotels || [],
          buses: busRes.buses || [],
          tickets: ticketRes.tickets || [],
        });
      }
    } catch (err) {
      if (err.response?.status === 404) {
        setError(`Mission not found for team: ${team}`);
      } else {
        setError(
          err.response?.data?.detail ||
          err.message ||
          'Replanning failed'
        );
      }
    } finally {
      setLoading(false);
    }
  }

  function handleSaveRecommendation() {
    if (!result?.recommendation) return;

    try {
      const saved = JSON.parse(localStorage.getItem('saved_recommendations') || '[]');
      const newRec = {
        ...result.recommendation,
        team,
        saved_at: new Date().toISOString(),
      };

      if (!saved.some((rec) => rec.city === newRec.city && rec.team === newRec.team)) {
        saved.push(newRec);
        localStorage.setItem('saved_recommendations', JSON.stringify(saved));
      }
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to save recommendation:', err);
    }
  }

  const recCity = result?.recommendation?.city;
  const startCity = mission?.itinerary?.[mission.itinerary.length - 1]?.city || 'Miami';

  return (
    <div id="replanning-page" className="map-layout">
      <HeroReplanning 
        team={team} 
        onReplan={handleReplan} 
        loading={loading} 
      />

      <div className="map-grid">
        <div className="map-sidebar">
          <section className="page-header" style={{ marginTop: 0 }}>
            <div>
              <p className="eyebrow">Intel dashboard</p>
              <h1>AI Replanning</h1>
            </div>
            {result && !savedSuccess && (
              <button className="btn" onClick={handleSaveRecommendation}>
                Save Route
              </button>
            )}
            {savedSuccess && (
              <button className="btn" style={{ background: 'var(--c-green)', color: '#000' }}>
                Saved!
              </button>
            )}
          </section>

          {!result && !loading && (
            <section className="card">
              <p className="description" style={{ marginBottom: '1.5rem' }}>
                Run the agent to recalculate routes and budgets based on the latest tournament developments.
              </p>
              <button className="btn" onClick={handleReplan}>
                Generate Plan
              </button>
            </section>
          )}

          {loading && (
            <section className="card">
              <p className="loading">Agent is analyzing routes and budgets...</p>
            </section>
          )}

          {error && (
            <div className="error-banner">{error}</div>
          )}

          {result && !loading && (
            <div className="stagger">
              <RecommendationCard recommendation={result.recommendation} />
              
              <div className="card">
                <div className="section-title">
                  <h3>Travel & Accommodations</h3>
                </div>
                <OptionsTable title="Flights" items={travelOptions.flights} empty="No flights found." />
                <OptionsTable title="Hotels (Aggregator)" items={travelOptions.hotels} empty="No hotels found." />
                <OptionsTable title="Bus Options" items={travelOptions.buses} empty="No buses found." />
                <OptionsTable title="Match Tickets" items={travelOptions.tickets} empty="No tickets found." />
              </div>

              <div className="card">
                <div className="section-title">
                  <h3>Map Controls</h3>
                </div>
                <div className="button-row">
                  <button className={`btn btn-small ${showRoute ? '' : 'btn-secondary'}`} onClick={() => setShowRoute(!showRoute)}>
                    {showRoute ? 'Hide Route' : 'Show Route'}
                  </button>
                  <button className={`btn btn-small ${showHotels ? '' : 'btn-secondary'}`} onClick={() => setShowHotels(!showHotels)}>
                    {showHotels ? 'Hide Hotels' : 'Show Hotels'}
                  </button>
                  <button className={`btn btn-small ${showFood ? '' : 'btn-secondary'}`} onClick={() => setShowFood(!showFood)}>
                    {showFood ? 'Hide Food' : 'Show Food'}
                  </button>
                </div>
              </div>

              <RankingTable result={result} />
              <ReasoningPanel result={result} />
              <AuditPanel result={result} />
            </div>
          )}
        </div>

        <div className="map-pane">
          {result && !loading ? (
            <MapView centerCity={recCity} height="100%">
              {showRoute && startCity && recCity && (
                <DirectionsRoute 
                  startCity={startCity} 
                  endCity={recCity} 
                />
              )}
              {showHotels && <HotelMap hotels={hotelsList} />}
              {showFood && <FoodMap venues={foodList} />}
            </MapView>
          ) : (
            <MapView centerCity={startCity} height="100%" />
          )}
        </div>
      </div>
    </div>
  );
}
