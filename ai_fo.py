import pandas as pd
from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

# -------------------------------
# Load Datasets
# -------------------------------
hotels = pd.read_csv("hotels.csv")
ngos = pd.read_csv("ngos.csv")

# -------------------------------
# AI Demand Prediction
# -------------------------------
# Predict daily food demand using past data
ngos["predicted_daily_demand"] = ngos["last_7day_demand_kg"] / 7

# -------------------------------
# AI Matching: Hotel → NGO
# -------------------------------
def recommend_ngo(hotel):
    ngos_copy = ngos.copy()

    ngos_copy["distance_km"] = ngos_copy.apply(
        lambda ngo: calculate_distance(
            hotel.latitude, hotel.longitude,
            ngo.latitude, ngo.longitude
        ), axis=1
    )

    # AI Priority Score (Urgency + Distance)
    ngos_copy["priority_score"] = (
        ngos_copy["predicted_daily_demand"] * 0.6 +
        (1 / (ngos_copy["distance_km"] + 1)) * 0.4
    )

    return ngos_copy.sort_values("priority_score", ascending=False).iloc[0]

# -------------------------------
# AI Matching: NGO → Hotel
# -------------------------------
def recommend_hotel(ngo):
    hotels_copy = hotels.copy()

    hotels_copy["distance_km"] = hotels_copy.apply(
        lambda hotel: calculate_distance(
            ngo.latitude, ngo.longitude,
            hotel.latitude, hotel.longitude
        ), axis=1
    )

    # AI Supply Score
    hotels_copy["supply_score"] = (
        hotels_copy["extra_food_kg"] * 0.7 +
        (1 / (hotels_copy["distance_km"] + 1)) * 0.3
    )

    return hotels_copy.sort_values("supply_score", ascending=False).iloc[0]

# -------------------------------
# Scenario 1: Hotel has extra food
# -------------------------------
print("\n🔹 HOTEL → NGO FOOD REDISTRIBUTION 🔹\n")

for _, hotel in hotels.iterrows():
    if hotel.extra_food_kg > 0:
        ngo = recommend_ngo(hotel)
        print(f"""
🚨 FOOD SURPLUS ALERT 🚨
Hotel: {hotel.hotel_name}
Location: {hotel.area}
Extra Food: {hotel.extra_food_kg} kg

➡ Recommended NGO:
NGO Name: {ngo.ngo_name}
Area: {ngo.area}
People Supported: {ngo.people_count}
Distance: {ngo.distance_km:.2f} km
""")

# -------------------------------
# Scenario 2: NGO has food shortage
# -------------------------------
print("\n🔹 NGO → HOTEL FOOD REQUEST 🔹\n")

for _, ngo in ngos.iterrows():
    if ngo.current_food_stock_kg < ngo.predicted_daily_demand:
        hotel = recommend_hotel(ngo)
        print(f"""
⚠️ FOOD SHORTAGE ALERT ⚠️
NGO: {ngo.ngo_name}
People Count: {ngo.people_count}
Current Stock: {ngo.current_food_stock_kg} kg

➡ Recommended Hotel:
Hotel Name: {hotel.hotel_name}
Area: {hotel.area}
Available Extra Food: {hotel.extra_food_kg} kg
Distance: {hotel.distance_km:.2f} km
""")
