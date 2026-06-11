// frontend/src/services/hotelService.js

const MOCK_HOTELS_DB = {
  "Miami": [
    { name: "Miami Beach Resort", rating: 4.5, address: "4833 Collins Ave, Miami Beach, FL 33140", price_level: 3, distance: "12.4 miles" },
    { name: "Eurostars Langford", rating: 4.2, address: "121 SE 1st St, Miami, FL 33131", price_level: 2, distance: "1.2 miles" },
    { name: "InterContinental Miami", rating: 4.7, address: "100 Chopin Plaza, Miami, FL 33131", price_level: 4, distance: "0.8 miles" }
  ],
  "Seattle": [
    { name: "The Edgewater Hotel", rating: 4.6, address: "2411 Alaskan Way, Seattle, WA 98121", price_level: 3, distance: "1.5 miles" },
    { name: "Green Tortoise Hostel", rating: 4.1, address: "105 Pike St, Seattle, WA 98101", price_level: 1, distance: "0.2 miles" },
    { name: "Sheraton Grand Seattle", rating: 4.5, address: "1400 6th Ave, Seattle, WA 98101", price_level: 3, distance: "0.4 miles" }
  ],
  "Los Angeles": [
    { name: "The Westin Bonaventure", rating: 4.4, address: "404 S Figueroa St, Los Angeles, CA 90071", price_level: 3, distance: "0.5 miles" },
    { name: "Freehand Los Angeles", rating: 4.2, address: "416 W 8th St, Los Angeles, CA 90014", price_level: 2, distance: "0.9 miles" },
    { name: "Beverly Hills Hotel", rating: 4.9, address: "9641 Sunset Blvd, Beverly Hills, CA 90210", price_level: 4, distance: "8.2 miles" }
  ],
  "Kansas City": [
    { name: "Loews Kansas City", rating: 4.7, address: "1515 Wyandotte St, Kansas City, MO 64108", price_level: 3, distance: "0.3 miles" },
    { name: "Hotel Phillips", rating: 4.4, address: "106 W 12th St, Kansas City, MO 64105", price_level: 2, distance: "0.6 miles" }
  ]
};

export async function searchHotels(city) {
  // If real Google Maps PlacesService is available in the window, we could query it.
  // Since we are not integrating paid live providers yet, we utilize our mock database.
  const normalizedCity = city || "Miami";
  
  // Try exact match first
  const match = Object.keys(MOCK_HOTELS_DB).find(
    k => k.toLowerCase() === normalizedCity.toLowerCase()
  );
  
  if (match) {
    return MOCK_HOTELS_DB[match];
  }

  // Procedural generator for host cities not explicitly configured
  return [
    {
      name: `${normalizedCity} Fan Plaza Hotel`,
      rating: 4.4,
      address: `100 Fan Boulevard, ${normalizedCity}`,
      price_level: 2,
      distance: "1.1 miles"
    },
    {
      name: `${normalizedCity} Grand Arena Suites`,
      rating: 4.6,
      address: `45 Stadium Way, ${normalizedCity}`,
      price_level: 3,
      distance: "0.4 miles"
    },
    {
      name: `Budget Inn ${normalizedCity}`,
      rating: 3.9,
      address: `900 Route 6, ${normalizedCity}`,
      price_level: 1,
      distance: "4.2 miles"
    }
  ];
}
