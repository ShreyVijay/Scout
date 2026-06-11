// frontend/src/services/foodService.js

const MOCK_FOOD_DB = {
  "Miami": [
    { name: "La Carreta (Cuban)", rating: 4.3, address: "3632 SW 8th St, Miami, FL 33135", category: "Restaurants", price_level: 2 },
    { name: "Panther Coffee", rating: 4.5, address: "2390 NW 2nd Ave, Miami, FL 33127", category: "Cafes", price_level: 2 },
    { name: "Love Life Cafe (Plant-based)", rating: 4.7, address: "2612 NW 5th Ave, Miami, FL 33127", category: "Vegan", price_level: 3 },
    { name: "Plant Theory Co.", rating: 4.4, address: "723 Lincoln Ln N, Miami Beach, FL 33139", category: "Vegetarian", price_level: 2 },
    { name: "Vice City Burgers", rating: 4.2, address: "1040 North Miami Avenue, Miami, FL 33136", category: "Fast Food", price_level: 1 }
  ],
  "Seattle": [
    { name: "Pike Place Chowder", rating: 4.7, address: "1530 Post Alley, Seattle, WA 98101", category: "Restaurants", price_level: 2 },
    { name: "Storyville Coffee", rating: 4.6, address: "94 Pike St, Seattle, WA 98101", category: "Cafes", price_level: 2 },
    { name: "Plum Bistro", rating: 4.5, address: "1429 12th Ave, Seattle, WA 98122", category: "Vegan", price_level: 3 },
    { name: "Cafe Flora", rating: 4.6, address: "2901 E Madison St, Seattle, WA 98112", category: "Vegetarian", price_level: 2 },
    { name: "Dick's Drive-In", rating: 4.4, address: "115 Broadway East, Seattle, WA 98102", category: "Fast Food", price_level: 1 }
  ],
  "Los Angeles": [
    { name: "Philippe The Original", rating: 4.5, address: "1001 Alameda St, Los Angeles, CA 90012", category: "Restaurants", price_level: 1 },
    { name: "Blue Bottle Coffee", rating: 4.4, address: "582 Mate St, Los Angeles, CA 90013", category: "Cafes", price_level: 2 },
    { name: "Crossroads Kitchen", rating: 4.7, address: "8284 Melrose Ave, Los Angeles, CA 90046", category: "Vegan", price_level: 3 },
    { name: "Sadaf Restaurant", rating: 4.3, address: "1624 Westwood Blvd, Los Angeles, CA 90024", category: "Vegetarian", price_level: 2 },
    { name: "In-N-Out Burger", rating: 4.6, address: "9149 S Sepulveda Blvd, Los Angeles, CA 90045", category: "Fast Food", price_level: 1 }
  ]
};

export async function searchFood(city, category = null) {
  const normalizedCity = city || "Miami";
  
  // Try exact match
  const match = Object.keys(MOCK_FOOD_DB).find(
    k => k.toLowerCase() === normalizedCity.toLowerCase()
  );
  
  let venues = [];
  if (match) {
    venues = MOCK_FOOD_DB[match];
  } else {
    // Procedural generation
    venues = [
      { name: `${normalizedCity} Diner`, rating: 4.2, address: `200 Main St, ${normalizedCity}`, category: "Restaurants", price_level: 2 },
      { name: `Roasters Coffee ${normalizedCity}`, rating: 4.5, address: `34 Brew Lane, ${normalizedCity}`, category: "Cafes", price_level: 1 },
      { name: `Green Garden Cafe`, rating: 4.4, address: `70 Healthy St, ${normalizedCity}`, category: "Vegetarian", price_level: 2 },
      { name: `Purely Plant Bistro`, rating: 4.6, address: `12 Vegan Blvd, ${normalizedCity}`, category: "Vegan", price_level: 3 },
      { name: `Express Bites`, rating: 4.0, address: `99 Stadium Access Road, ${normalizedCity}`, category: "Fast Food", price_level: 1 }
    ];
  }

  if (category) {
    return venues.filter(v => v.category.toLowerCase() === category.toLowerCase());
  }
  return venues;
}
