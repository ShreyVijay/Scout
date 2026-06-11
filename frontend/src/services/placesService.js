let placesServiceInstance = null;

function getService() {
  if (placesServiceInstance) return placesServiceInstance;
  if (!window.google || !window.google.maps || !window.google.maps.places) return null;
  
  // We need a dummy DOM element for the PlacesService constructor
  const dummyElement = document.createElement('div');
  placesServiceInstance = new window.google.maps.places.PlacesService(dummyElement);
  return placesServiceInstance;
}

function processResults(results) {
  return results.map(place => ({
    name: place.name,
    rating: place.rating || 0,
    vicinity: place.vicinity || place.formatted_address || '',
    price_level: place.price_level || 1,
    photo_url: place.photos && place.photos.length > 0 ? place.photos[0].getUrl({ maxWidth: 400 }) : null,
    place_id: place.place_id
  }));
}

export async function searchHotels(city, lat, lng) {
  const service = getService();
  if (!service || !lat || !lng) return [];

  return new Promise((resolve) => {
    service.nearbySearch(
      {
        location: new window.google.maps.LatLng(lat, lng),
        radius: 8000,
        type: 'lodging',
      },
      (results, status) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK && results) {
          resolve(processResults(results));
        } else {
          resolve([]);
        }
      }
    );
  });
}

export async function searchFood(city, lat, lng) {
  const service = getService();
  if (!service || !lat || !lng) return [];

  return new Promise((resolve) => {
    service.nearbySearch(
      {
        location: new window.google.maps.LatLng(lat, lng),
        radius: 5000,
        type: 'restaurant',
      },
      (results, status) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK && results) {
          resolve(processResults(results));
        } else {
          resolve([]);
        }
      }
    );
  });
}

export async function getStadiumPhoto(stadiumName) {
  const service = getService();
  if (!service || !stadiumName) return null;

  return new Promise((resolve) => {
    service.textSearch(
      {
        query: stadiumName,
      },
      (results, status) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK && results && results.length > 0) {
          const place = results[0];
          if (place.photos && place.photos.length > 0) {
            resolve(place.photos[0].getUrl({ maxWidth: 800 }));
            return;
          }
        }
        resolve(null);
      }
    );
  });
}

export async function getCityPhoto(cityName) {
  const service = getService();
  if (!service || !cityName) return null;

  return new Promise((resolve) => {
    service.textSearch(
      {
        query: `${cityName} skyline landmark`,
      },
      (results, status) => {
        if (status === window.google.maps.places.PlacesServiceStatus.OK && results && results.length > 0) {
          const place = results[0];
          if (place.photos && place.photos.length > 0) {
            resolve(place.photos[0].getUrl({ maxWidth: 800 }));
            return;
          }
        }
        resolve(null);
      }
    );
  });
}
