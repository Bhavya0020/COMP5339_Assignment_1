import pandas as pd
from geopy.geocoders import Nominatim
from rapidfuzz import process, fuzz
from time import sleep

df = pd.read_csv("processed_data.csv")
df_geo = pd.read_csv("147635_01_0.csv")

df["address"] = df["address"].astype(str).str.strip()
df["servicestationname_clean"] = df["servicestationname"].astype(str).str.lower().str.strip()
df_geo["station_name_clean"] = df_geo["STATION_NAME"].astype(str).str.lower().str.strip()
df_geo["STATION_OWNER"] = df_geo["STATION_OWNER"].astype(str).str.strip()

geolocator = Nominatim(user_agent="fuelcheck-geocoder")
unique_addresses = df["address"].dropna().unique()
geocoded = []

print(f"Geocoding {len(unique_addresses)} unique addresses...")

for i, address in enumerate(unique_addresses):
    try:
        location = geolocator.geocode(address + ", NSW, Australia", timeout=10)
        if location:
            geocoded.append({"address": address, "latitude": location.latitude, "longitude": location.longitude})
        else:
            geocoded.append({"address": address, "latitude": None, "longitude": None})
    except:
        geocoded.append({"address": address, "latitude": None, "longitude": None})
    sleep(1)

df_lookup = pd.DataFrame(geocoded)
df = df.merge(df_lookup, on="address", how="left")

exact_match = pd.merge(df, df_geo[["station_name_clean", "STATION_OWNER"]],
                       left_on="servicestationname_clean", right_on="station_name_clean", how="left")

geo_lookup = dict(zip(df_geo["station_name_clean"], df_geo["STATION_OWNER"]))

def fuzzy_lookup(name):
    match, score, _ = process.extractOne(name, geo_lookup.keys(), scorer=fuzz.token_sort_ratio)
    return geo_lookup[match] if score >= 90 else None

exact_match["station_owner"] = exact_match["STATION_OWNER"]
missing = exact_match["station_owner"].isna()
exact_match.loc[missing, "station_owner"] = exact_match.loc[missing, "servicestationname_clean"].apply(fuzzy_lookup)

def classify_fuel(fuelcode):
    fuelcode = str(fuelcode).strip().upper()
    if fuelcode in ["E10", "U91"]:
        return "Regular Unleaded"
    elif fuelcode in ["P95", "P98"]:
        return "Premium Unleaded"
    elif fuelcode == "DL":
        return "Diesel"
    elif fuelcode == "PDL":
        return "Premium Diesel"
    elif fuelcode == "LPG":
        return "Gas"
    elif fuelcode == "E85":
        return "Ethanol Blend"
    else:
        return "Not Defined"

exact_match["fuel_category"] = exact_match["fuelcode"].apply(classify_fuel)
exact_match.drop(columns=["servicestationname_clean", "station_name_clean", "STATION_OWNER"], inplace=True)
exact_match.to_csv("augmented_fuelcheck_data.csv", index=False)









