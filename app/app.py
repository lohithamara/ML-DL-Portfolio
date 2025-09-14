from flask import Flask, render_template, request
from datetime import datetime

import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.inference import predict_price

app = Flask(__name__)

# Example options (can be loaded from columns.json or hardcoded)
AIRLINES = ["Air India", "GO FIRST", "Indigo", "SpiceJet", "Vistara"]
CITIES = ["Chennai", "Delhi", "Hyderabad", "Kolkata", "Mumbai"]
CLASSES = ["Economy", "Business"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form
        source = data.get("source_city")
        destination = data.get("destination_city")
        journey_date = data.get("journey_date")
        persons = int(data.get("persons", 1))
        travel_class = data.get("class")
        today = datetime.now().date()
        journey = datetime.strptime(journey_date, "%Y-%m-%d").date()
        days_left = (journey - today).days
        # Generate random flights
        flights = generate_flights(source, destination, journey_date, persons, travel_class)
        return render_template("results.html", flights=flights, days_left=days_left, persons=persons, filters={
            "airlines": AIRLINES,
            "classes": CLASSES
        })
    from datetime import date
    today = date.today().isoformat()
    return render_template("index.html", cities=CITIES, classes=CLASSES, today=today)

def generate_flights(source, destination, journey_date, persons, travel_class):
    flights = []
    now = datetime.now()
    today = now.date()
    journey = datetime.strptime(journey_date, "%Y-%m-%d").date()
    # City-to-city base durations in minutes
    city_durations = {
        ("Chennai", "Delhi"): 170, ("Chennai", "Hyderabad"): 75, ("Chennai", "Kolkata"): 130, ("Chennai", "Mumbai"): 110,
        ("Delhi", "Hyderabad"): 120, ("Delhi", "Kolkata"): 125, ("Delhi", "Mumbai"): 125,
        ("Hyderabad", "Kolkata"): 115, ("Hyderabad", "Mumbai"): 85,
        ("Kolkata", "Mumbai"): 150
    }
    for _ in range(10):
        airline = random.choice(AIRLINES)
        # Randomly assign class for each flight
        flight_class = random.choice(['Economy', 'Business'])
        # If journey is today, only allow future departure times
        if journey == today:
            min_hour = now.hour
        else:
            min_hour = 0
        dep_hour = random.randint(min_hour, 23)
        # If journey is today and dep_hour is now.hour, only allow future minutes
        if journey == today and dep_hour == now.hour:
            possible_minutes = [m for m in [0, 15, 30, 45] if m > now.minute]
            if not possible_minutes:
                dep_hour = min(dep_hour + 1, 23)
                dep_minute = 0
            else:
                dep_minute = random.choice(possible_minutes)
        else:
            dep_minute = random.choice([0, 15, 30, 45])
        dep_time = f"{dep_hour:02d}:{dep_minute:02d}"
        # Get base duration for city pair (or reverse)
        base_duration = city_durations.get((source, destination))
        if base_duration is None:
            base_duration = city_durations.get((destination, source), 120)  # fallback 2hr
        # Add random +/- 10 min
        duration = base_duration + random.randint(-10, 10)
        # Add 40 min per stop
        stops = random.choice([0, 1, 2])
        duration += stops * 40
        # Calculate arrival time
        arr_total_min = dep_hour * 60 + dep_minute + duration
        arr_hour = (arr_total_min // 60) % 24
        arr_minute = arr_total_min % 60
        arr_time = f"{int(arr_hour):02d}:{int(arr_minute):02d}"
        # Prepare input for model
        input_dict = {
            'stops': stops,
            'duration': duration,
            'days_left': (journey - today).days,
            'airline': airline,
            'source_city': source,
            'departure_time': dep_time_to_label(dep_hour),
            'arrival_time': dep_time_to_label(arr_hour),
            'destination_city': destination,
            'class': flight_class
        }
        # Predict price for one person, then multiply
        price = predict_price(input_dict)
        total_price = int(price * persons)
        flights.append({
            "airline": airline,
            "source": source,
            "destination": destination,
            "departure": dep_time,
            "arrival": arr_time,
            "stops": stops,
            "class": flight_class,
            "price": total_price
        })
    return flights

# Helper to map hour to label (should match your model's encoding)
def dep_time_to_label(hour):
    if 5 <= hour < 8:
        return "Early_Morning"
    elif 8 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Evening"
    elif 17 <= hour < 21:
        return "Night"
    else:
        return "Late_Night"

if __name__ == "__main__":
    app.run(debug=True)
