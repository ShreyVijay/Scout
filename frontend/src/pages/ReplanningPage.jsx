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
import { searchHotels } from '../services/hotelService';
import { searchFood } from '../services/foodService';
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
        const hotels = await searchHotels(recCity);
        const food = await searchFood(recCity);
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
    <div id="replanning-page" className="page">
      <section className="page-header">
        <div>
          <p className="eyebrow">Route update</p>
          <h1>Replanning: {team}</h1>
        </div>
        <RouterLink
          to={`/mission/${encodeURIComponent(team)}`}
          className="btn btn-secondary"
          id="link-back-mission"
        >
          Back to Mission
        </RouterLink>
      </section>

      <HeroReplanning 
        team={team} 
        onReplan={handleReplan} 
        loading={loading} 
      />

      {error && <div className="error-banner">{error}</div>}

      {result && recCity && (
        <div id="recommendation-map-section" className="page">
          <section className="card">
            <div className="section-title">
              <h2>Interactive Recommendation Map</h2>
              <span className="badge">{startCity} to {recCity}</span>
            </div>

            <div className="control-row">
              <label>
                <input
                  type="checkbox"
                  checked={showRoute}
                  onChange={(e) => setShowRoute(e.target.checked)}
                />
                Show Route
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={showHotels}
                  onChange={(e) => setShowHotels(e.target.checked)}
                />
                Show Hotels
              </label>
              <label>
                <input
                  type="checkbox"
                  checked={showFood}
                  onChange={(e) => setShowFood(e.target.checked)}
                />
                Show Food Spots
              </label>
            </div>

            <MapView centerCity={recCity} height="420px">
              {showRoute && <DirectionsRoute startCity={startCity} endCity={recCity} />}
              {showHotels && <HotelMap hotels={hotelsList} city={recCity} />}
              {showFood && <FoodMap venues={foodList} city={recCity} />}
            </MapView>
          </section>

          <div className="grid-2">
            <div className="page">
              <RecommendationCard recommendation={result.recommendation} />
              <section className="card">
                <button className="btn" onClick={handleSaveRecommendation}>
                  Save Recommendation
                </button>
                {savedSuccess && (
                  <p className="success-banner">Saved to dashboard.</p>
                )}
              </section>
            </div>

            <section className="card">
              <div className="section-title">
                <h2>Travel Intelligence</h2>
              </div>
              <OptionsTable
                title={`Flights from ${startCity}`}
                empty="No flights loaded."
                items={travelOptions.flights}
              />
              <OptionsTable
                title={`Hotels in ${recCity}`}
                empty="No lodging search results."
                items={travelOptions.hotels}
                priceLabel="Rate"
              />
              <OptionsTable
                title={`Buses from ${startCity}`}
                empty="No bus routes found."
                items={travelOptions.buses}
              />
              <OptionsTable
                title="Match Tickets"
                empty="No tickets listed."
                items={travelOptions.tickets}
              />
            </section>
          </div>

          <RankingTable rankings={result.rankings} />
          <ReasoningPanel reasoning={result.reasoning} />
          <AuditPanel audit={result.audit} />
        </div>
      )}
    </div>
  );
}
