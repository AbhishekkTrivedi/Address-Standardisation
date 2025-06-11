from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time

geolocator = Nominatim(user_agent="city-alias-checker")

def get_coordinates(city_name, country="India"):
    """Fetch coordinates of a city using geopy and Nominatim."""
    try:
        time.sleep(1)  # Nominatim API rate limit
        location = geolocator.geocode(f"{city_name}, {country}")
        if location:
            return (location.latitude, location.longitude)
    except Exception as e:
        print(f"Error fetching {city_name}: {e}")
    return None

def are_same_city(city_names, threshold=1000):
    """Returns whether all city names refer to the same city based on coordinates."""
    coords = {}

    # Step 1: Get coordinates for each city
    for name in city_names:
        coord = get_coordinates(name)
        if coord:
            coords[name] = coord
        else:
            print(f"❌ Could not geocode: {name}")

    if len(coords) < 2:
        print("⚠️ Need at least 2 valid cities to compare.")
        return False

    # Step 2: Compare each city with the first one
    ref_city, ref_coord = list(coords.items())[0]
    for name, coord in list(coords.items())[1:]:
        dist = geodesic(ref_coord, coord).meters
        print(f"📍 {ref_city} ↔ {name} = {dist:.2f} meters")
        if dist > threshold:
            return False

    return True

------inputs-----------------------------------------------

city_list1 = ["Allahabad", "Prayagraj"]
print("✅ Same City?" , are_same_city(city_list1))

city_list2 = ["Delhi", "Mumbai"]
print("✅ Same City?" , are_same_city(city_list2))

city_list3 = ["Madras", "Chennai"]
print("✅ Same City?" , are_same_city(city_list3))

city_list4 = ["Varanasi", "Banaras","Kashi"]
print("✅ Same City?" , are_same_city(city_list4))

