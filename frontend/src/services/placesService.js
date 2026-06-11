let placesServiceInstance = null;

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

function apiPhotoUrl(query) {
  if (!query) return null;
  return `${API_BASE_URL}/google/place-photo?query=${encodeURIComponent(query)}`;
}

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

const STADIUM_PHOTOS = {
  "MetLife Stadium": "/images/BYoXUwWz53m5u3wjg3KieATeruWOJG9ygEfjRG4Erz4jm5NIgPKUsnyo7naSxmmVjUXARqivF-4OePYYiLJvpk2W_Ou2f3u75iCfGCIcZPrRqIrz1BOM__uaQL_L2OmDBM6eUewlWoLiGwZJUnpFYPIrnA2KIOID67rYbwtAF_8.jpg",
  "AT&T Stadium": "/images/M6BnNk6ithvOLLWj_PnvNZZ3m0azLADZ4kpo50NPEMQPxDuebIFSQzZoFxatgVpjH30KVBiFncts9OwPRjDqKD9SJLQOcu5P297KnXZcjxEO8xodn9k6VSxxlYbALgArhT-XKC53nCfPb5q3sVVsesT3WEYoBWty0NJXVTeREZMal4KJEBF0qInCFywPnYdK.jpg",
  "SoFi Stadium": "/images/NaTqRBXVO5d7b0iS0BqV0RPrqXc5yi2mMx2qzKoL6JyrAQkDFR-OCaTgLR4DzNGpHiIxQS3T7JNzO6lUTBVRb-TLLSIlsHDaMLyn87kdcQDaE7bWBKN7l8-t4fMrxcd0tHEt6beMOLu_ezpjdxJdSW-FDLzXIzLgw89Yw5sA-YhS3h5UsFzYQcHv1oImgMqd.jpg",
  "Hard Rock Stadium": "/images/5wEB8yxSEgHc5wNtu3gwku_XQw2LIOD1OdsNWcjjQfaocYSNJHqbUjINYuVreLKJCLfnOgVSuSVZMGEmaxG-08FCmg65MgNC6dNZe0qzHILaJzbZX2PKU7Ee-zUMG29Br7fcXVTzkzXfaqlMZkBhJq8ve0c5gUEVPv2pU3lMegYRON177BN2LTYDQTxNlWtv.jpg",
  "Mercedes-Benz Stadium": "/images/46-KSmm7rLCIVqZ5N6wcMCKtPtvl5-JpdfwzWFH9xaAkVbMujRf3K063na8nQcsyXjvhnw-WAm8RW6xwXkEMLyDxZvdT3UV5c0yJdD66m0Scl1Q_lKiZ7OraRTqxXvPNbx05hrKzZM2XYFf-pyJE0Mk7hW-hp6BzLCyEgeql_oMTpXJ1nNiF-jpe2JPc4fbg.jpg",
  "NRG Stadium": "/images/LzawP426H81hXQ__gHaZ7H90REydhmv1zQACdJcU1D9PpKpBpu29ejYrJGpSVgvrj2hIVvryN7VgVGR5y9lbaaDyYqMCwxK39igq4x3_c7SY2SVDCYmXGB469XwyUzZfvNIavWF3yT6c5EfEMspCkr2zzWyZ2Kr7C3wngdPE5_o.jpg",
  "Lumen Field": "/images/AuMhZM0mQNZafJcGwvjhAa40HMJe6RW3eZMmjq3qhbGNF82KsnJIiiaZcZ9Kad_RmqybN8CN2gFDG3ezGBqP1cWiMWmi6jK11Zt2g9t1ts_7mzruLy8fXx4pW1FQ1na5__KKBicjkAKbRPylKWUftlhdszk1a6hIsSpgOvxn8lG4uE97jpc_Z6W5XkbyioMe.jpg",
  "Gillette Stadium": "/images/LAk3gmFzKzLBqd1qp4ZN-Kmm2eZ0hhbCSBE6U4MUOzkl83IFfdLF0pNXdYYzUlUdLilL40Vb7rKHl3BfIfa3_jwm3fv-tA9eFWTbhrdADebwWXWyqtNpHrH-whdDbYrkK20QK5vJEp8HdWJssIW-Nnsu1IG7S5_qfH3t33dh23A.jpg",
  "GEHA Field at Arrowhead Stadium": "/images/99r1ctc_yN3QnhQtkXD3dqrs_tGYBWXwC5k48mFPwW5HSUL9wPAu5lMyzTyVhqwy1RQof7Nez_d0_uZUVatyoo_ESxOqo0ixYOx82wRh5nYLx3HAZmEM48zKYclVTnbJnjhn5bWEWgZ3b-KamIShQTNwTh7rW44Oj72tdG1zvYU.jpg"
};

const CITY_PHOTOS = {
  "Atlanta": "/images/O0j1e3YzD9NE8c-lBEIRkgx_-vSdhmLqBvoGP83EG_zr3wUw0l04GyllNtVrZFxJJVdzYPYjYLp5iVc7xn7X36_iZHqrSymxjJ-at5_qRN7xNeftHgo4CyvlJ2q4tgHuWzb68NlqAviQ2bqF5ajzbJsLafFtw6ifw1rCsKGv1qM.jpg",
  "Boston": "/images/ZRHGE5tZWwXDwWZv6D81YOKFE0wIRzm6RplamAql3NF9e45Ah3Oe_cUrVNmrN6wHTieynulxH_0-16k--6LpcBnF1YDWmwUwJBK3VbyGqZdLNC7NjxO09_ODgenfaxywszQRTVi2OCPxnHMgjw8qf25g6A2Z5bK0XoQjLMgFys8.jpg",
  "Dallas": "/images/biEq54AyPPzGq_V5_r4lRmujPWwwzt6XBlNqi9y8B7Jhhj8dSm0F7WUQ8rALiZvU5ZU_zm_f6nFMGkTyjK6r4ieUweUHyUNniSZX4eD48gpze2T3DZxi1OhU6_FI-Rh0EviKo6m-aToQamcru1k7HF8fZfCthTEEi1q4VAAa59I.jpg",
  "Houston": "/images/eK6vNnn_N7m2JPCqWHkvqWqwK45QlX85oGwtToG4k4d0ijfIAsd_rGoPa4KdFdAYdh4_r_unKg0oieGuumgvRlXQKcPU4kt58VXbRlIZ76KfmliYgDDL3PhYZ0mfoW7EV1yeHqjUmdDg16nFFacn-2LgFP8lUwTUCmbJnR1Uo8uaFgh_ZcQ5tJZhSFceP5sh.jpg",
  "Kansas City": "/images/pmHp5QXNQXBaEMD0EdhK3UsQftrpltvWsM3aJ-JftOgaste7T71ySXZeU6VSsfv1EUNLs05DYEtesSiqy7uoe_Wr9cnLni1UXq3yevab58QcjSlsS7e1NH06JOEvZOp3GOqRfrjPCAXg9ofpWyaV55YNqjl8UiAPv7CyQr6HHLU.jpg",
  "Los Angeles": "/images/vnsQoS1-F0Vz_ys9-tmoeUfr0T61q9Pd_fv15H6gFd_LLTHM8HVqxA6jReIdblxWpA2OEerWJeboStS7DYXTvQd2MadiWubgt_pvePtcCdT8Pgy2glgsOLdOmXvyOaIwowhyScqR_OquvFaBNb5rCDzM-GlU_sD7Hh81X7qSxOC31Dox-sqDFwP8Dsu6eXvG.jpg",
  "Miami": "/images/xJ_-F-ta1P0YjR0VI7ZzxIoQK3yshxTJ3ztKwx0tLmTVafYSX9YFj6TOPcvmliuxRAm_Y875WCQv8PtCGuxH4PKhHdd39vSPyqprCdRnYYeA80HURp_otB03JRHDVIq6RLf92dEqeP_lEPlc2j6mjm8gRPXeVSy6REHlTQRyW85gKjgSHvfq06cez15MwwMN.jpg",
  "New York": "/images/BYoXUwWz53m5u3wjg3KieATeruWOJG9ygEfjRG4Erz4jm5NIgPKUsnyo7naSxmmVjUXARqivF-4OePYYiLJvpk2W_Ou2f3u75iCfGCIcZPrRqIrz1BOM__uaQL_L2OmDBM6eUewlWoLiGwZJUnpFYPIrnA2KIOID67rYbwtAF_8.jpg",
  "Seattle": "/images/AuMhZM0mQNZafJcGwvjhAa40HMJe6RW3eZMmjq3qhbGNF82KsnJIiiaZcZ9Kad_RmqybN8CN2gFDG3ezGBqP1cWiMWmi6jK11Zt2g9t1ts_7mzruLy8fXx4pW1FQ1na5__KKBicjkAKbRPylKWUftlhdszk1a6hIsSpgOvxn8lG4uE97jpc_Z6W5XkbyioMe.jpg",
  "New York/New Jersey": "/images/BYoXUwWz53m5u3wjg3KieATeruWOJG9ygEfjRG4Erz4jm5NIgPKUsnyo7naSxmmVjUXARqivF-4OePYYiLJvpk2W_Ou2f3u75iCfGCIcZPrRqIrz1BOM__uaQL_L2OmDBM6eUewlWoLiGwZJUnpFYPIrnA2KIOID67rYbwtAF_8.jpg"
};

export async function getStadiumPhoto(stadiumName) {
  if (stadiumName && STADIUM_PHOTOS[stadiumName]) {
    return STADIUM_PHOTOS[stadiumName];
  }

  const backendUrl = apiPhotoUrl(stadiumName);
  if (backendUrl) return backendUrl;

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
  if (cityName && CITY_PHOTOS[cityName]) {
    return CITY_PHOTOS[cityName];
  }

  const backendUrl = apiPhotoUrl(`${cityName} skyline landmark`);
  if (backendUrl) return backendUrl;

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

