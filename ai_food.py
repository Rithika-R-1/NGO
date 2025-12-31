# ============================================
# AI FOOD REDISTRIBUTION SYSTEM
# Domain: NGO / Social Welfare / AIDS
# ============================================

import math
import time
from datetime import datetime

# --------------------------------------------
# Utility Functions
# --------------------------------------------

def log(message):
    """Safe logging without Unicode characters"""
    print(f"[{datetime.now()}] {message}")

def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine formula for distance in KM"""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

# --------------------------------------------
# AI FUNCTIONS
# --------------------------------------------

def predict_ngo_demand(people_count):
    """
    AI Demand Prediction
    Average food requirement = 0.6 kg per person
    """
    return round(people_count * 0.6, 2)

def calculate_priority_score(predicted_demand, distance, current_stock):
    """
    AI Decision Intelligence
    """
    fairness_score = predicted_demand / (current_stock + 1)

    priority_score = (
        0.5 * predicted_demand +
        0.3 * (1 / (distance + 1)) +
        0.2 * fairness_score
    )

    return round(priority_score, 3)

# --------------------------------------------
# USER INPUT MODULES
# --------------------------------------------

def hotel_user_input():
    print("\n--- HOTEL INPUT ---")
    name = input("Hotel Name: ")
    surplus = float(input("Surplus food available (kg): "))
    lat = float(input("Hotel Latitude: "))
    lon = float(input("Hotel Longitude: "))

    return {
        "name": name,
        "surplus": surplus,
        "lat": lat,
        "lon": lon
    }

def ngo_user_input():
    print("\n--- NGO INPUT ---")
    name = input("NGO Name: ")
    people = int(input("People to be served today: "))
    stock = float(input("Current food stock (kg): "))
    lat = float(input("NGO Latitude: "))
    lon = float(input("NGO Longitude: "))

    return {
        "name": name,
        "people": people,
        "stock": stock,
        "lat": lat,
        "lon": lon
    }

# --------------------------------------------
# AI MATCHING LOGIC
# --------------------------------------------

def match_hotel_to_ngos(hotel, ngos):
    log("Running Hotel -> NGO AI matching...")

    best_match = None
    best_score = -1

    for ngo in ngos:
        distance = calculate_distance(
            hotel["lat"], hotel["lon"],
            ngo["lat"], ngo["lon"]
        )

        predicted_demand = predict_ngo_demand(ngo["people"])

        score = calculate_priority_score(
            predicted_demand,
            distance,
            ngo["stock"]
        )

        if score > best_score and hotel["surplus"] >= predicted_demand:
            best_score = score
            best_match = {
                "ngo": ngo,
                "distance": distance,
                "predicted_demand": predicted_demand,
                "score": score
            }

    return best_match

def match_ngo_to_hotels(ngo, hotels):
    log("Running NGO -> Hotel AI matching...")

    best_match = None
    best_score = -1

    for hotel in hotels:
        distance = calculate_distance(
            ngo["lat"], ngo["lon"],
            hotel["lat"], hotel["lon"]
        )

        supply_score = hotel["surplus"] / (distance + 1)

        if supply_score > best_score:
            best_score = supply_score
            best_match = {
                "hotel": hotel,
                "distance": distance,
                "supply_score": round(supply_score, 2)
            }

    return best_match

# --------------------------------------------
# MAIN SYSTEM FLOW
# --------------------------------------------

def main():
    log("AI Food Redistribution System Started")

    ngos = []
    hotels = []

    while True:
        print("\n--- MENU ---")
        print("1. Register Hotel Surplus")
        print("2. Register NGO Requirement")
        print("3. Run Hotel -> NGO Matching")
        print("4. Run NGO -> Hotel Matching")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            hotel = hotel_user_input()
            hotels.append(hotel)
            log("Hotel registered successfully.")

        elif choice == "2":
            ngo = ngo_user_input()
            ngos.append(ngo)
            log("NGO registered successfully.")

        elif choice == "3":
            if not hotels or not ngos:
                log("Insufficient data to run matching.")
                continue

            for hotel in hotels:
                match = match_hotel_to_ngos(hotel, ngos)
                if match:
                    print("\nALERT:")
                    print(f"Hotel: {hotel['name']}")
                    print(f"Recommended NGO: {match['ngo']['name']}")
                    print(f"Distance: {match['distance']} km")
                    print(f"Predicted Demand: {match['predicted_demand']} kg")
                    print(f"Priority Score: {match['score']}")
                else:
                    print("\nNo suitable NGO found.")

        elif choice == "4":
            if not hotels or not ngos:
                log("Insufficient data to run matching.")
                continue

            for ngo in ngos:
                match = match_ngo_to_hotels(ngo, hotels)
                if match:
                    print("\nALERT:")
                    print(f"NGO: {ngo['name']}")
                    print(f"Recommended Hotel: {match['hotel']['name']}")
                    print(f"Distance: {match['distance']} km")
                else:
                    print("\nNo suitable Hotel found.")

        elif choice == "5":
            log("System shutting down.")
            break

        else:
            print("Invalid choice. Try again.")

        time.sleep(1)

# --------------------------------------------
# ENTRY POINT
# --------------------------------------------

if __name__ == "__main__":
    main()
