import requests
from geopy.distance import geodesic
from collections import Counter
from data import STATE_ISO_CODES, CLIENT_LOCATIONS

USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"

def fetch_usgs_data():
    """Get earthquake data from USGS for the past week."""
    try:
        response = requests.get(USGS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting data: {e}")
        return None

def extract_state_from_place(place):
    """Find the state ISO code from an earthquake location."""
    if not place or ',' not in place:
        return None
    parts = place.split(',')
    state_part = parts[-1].strip()
    for state, ISO in STATE_ISO_CODES.items():
        if state_part.upper() == ISO or state_part.lower() == state.lower():
            return ISO
    return None

def analyse_state_risk(earthquakes):
    """Count earthquakes and average magnitude by state, skipping Hawaii."""
    state_counts = Counter()
    state_magnitudes = {}
    
    for feature in earthquakes['features']:
        place = feature['properties']['place']
        mag = feature['properties']['mag']
        state = extract_state_from_place(place)
        
        if state and state != 'HI':
            state_counts[state] += 1
            if state not in state_magnitudes:
                state_magnitudes[state] = []
            state_magnitudes[state].append(mag)
    
    state_avg_mags = {state: sum(mags) / len(mags) for state, mags in state_magnitudes.items()}
    return state_counts, state_avg_mags

def assess_location_risk(earthquakes, locations, radius_km=50):
    """Check earthquake risk for client locations with a default radius of 50km."""
    risk_summary = {}
    
    for loc in locations:
        loc_coords = loc['coords']
        nearby_quakes = []
        
        for feature in earthquakes['features']:
            quake_coords = (feature['geometry']['coordinates'][1], feature['geometry']['coordinates'][0])
            distance = geodesic(loc_coords, quake_coords).kilometers
            if distance <= radius_km:
                nearby_quakes.append({
                    'mag': feature['properties']['mag'],
                    'distance_km': distance,
                    'place': feature['properties']['place']
                })
        
        risk_score = len(nearby_quakes) * (sum(quake['mag'] for quake in nearby_quakes) / len(nearby_quakes) if nearby_quakes else 0)
        risk_summary[loc['name']] = {
            'city': loc['city'],
            'nearby_quakes': len(nearby_quakes),
            'avg_magnitude': sum(quake['mag'] for quake in nearby_quakes) / len(nearby_quakes) if nearby_quakes else 0,
            'risk_score': risk_score
        }
    
    return risk_summary

def print_results(state_counts, state_avg_mags, location_risks):
    """Printing results to the console."""
    print("\n--- State Earthquake Risk (Past 7 Days) ---")
    if state_counts:
        most_active = state_counts.most_common(1)[0]
        print(f"Most active state: {most_active[0]} ({most_active[1]} events)")
        print("\nEarthquake counts by state:")
        for state, count in state_counts.most_common():
            avg_mag = state_avg_mags.get(state, 0)
            print(f"{state}: {count} events, Avg Magnitude: {avg_mag:.2f}")
    else:
        print("No data available.")
    
    print("\n--- Client Location Risks ---")
    for loc_name, risk in location_risks.items():
        print(f"\nBuilding: {loc_name} ({risk['city']})")
        print(f"Nearby Earthquakes (within 50km): {risk['nearby_quakes']}")
        print(f"Avg Magnitude: {risk['avg_magnitude']:.2f}")
        print(f"Risk Score: {risk['risk_score']:.2f}")

def main():
    data = fetch_usgs_data()
    if not data:
        return
    
    # Asking the user for a radius
    radius_input = input("Enter the radius in kilometers (e.g., 10, 50): ")
    try:
        radius_km = float(radius_input)  # Converts input to a number
        if radius_km <= 0:
            print("Radius must be positive. Using default 50km.")
            radius_km = 50
    except ValueError:
        print("Invalid input. Using default 50km.")
        radius_km = 50
    
    state_counts, state_avg_mags = analyse_state_risk(data)
    location_risks = assess_location_risk(data, CLIENT_LOCATIONS, radius_km) 
    print_results(state_counts, state_avg_mags, location_risks)

if __name__ == "__main__":
    main()