import pandas as pd
from geopy.geocoders import Nominatim
import time
import os

def augment_with_geolocation(df):
    geolocator = Nominatim(user_agent="fuelcheck_mapper")
    station_names = df["service_station_name"].dropna().unique()
    
    results = []
    for name in station_names:
        try:
            location = geolocator.geocode(f"{name}, NSW, Australia")
            if location:
                results.append({
                    "service_station_name": name,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
        time.sleep(1)  # Respect API rate limit

    loc_df = pd.DataFrame(results)
    os.makedirs("data", exist_ok=True)
    loc_df.to_csv("data/station_locations.txt", index=False)
    return loc_df
