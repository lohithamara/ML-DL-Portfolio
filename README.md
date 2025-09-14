# Flight Price Prediction Web App

A modern Flask web application for searching and comparing flight prices between major Indian cities. Users can enter journey details, view multiple flight options with realistic durations and prices (predicted by a trained ML model), and filter results by airline, stops, and class.


## Features
- Enter source, destination, journey date, and number of passengers
- Realistic flight durations and times based on city pairs
- Prices predicted by a machine learning model (not random)
- Filters for airline, stops, and class
- Responsive, modern UI with professional styling
- "Modify Search" option for easy re-query

## About the Model & Prediction Pipeline

This project uses a supervised machine learning model (Decision Tree or ANN) trained on a cleaned flight price dataset. The model predicts flight prices based on several features:

- **Numerical features:**
   - Number of stops
   - Duration (in minutes, based on city pair and stops)
   - Days left until journey
- **Categorical features (one-hot encoded):**
   - Airline
   - Source city
   - Destination city
   - Departure time (bucketed)
   - Arrival time (bucketed)
   - Class (Economy/Business)

### Preprocessing & Inference
- Numerical features are scaled using a `MinMaxScaler` (saved as `scaler.pkl`).
- Categorical features are one-hot encoded to match the model's training columns (`encoded_columns.pkl`).
- The model (`dt_model.pkl` or `ann_model.pkl`) is loaded and used to predict the price for each generated flight option.
- The prediction pipeline is implemented in `utils/inference.py` and called from the Flask app for each result.

### How Prediction Works in the App
1. User enters search details (cities, date, persons).
2. The app generates random but realistic flight options (airline, times, stops, class).
3. For each option, the model predicts the price using the above features.
4. The user sees a list of options with predicted prices and can filter by airline, stops, and class.

### Model Training
- Data cleaning, feature engineering, and model training are documented in the included Jupyter notebook.
- You can retrain the model with your own data and update the `.pkl` files for improved accuracy.

## Project Structure
```
models/                # Model and scaler files (not included in repo)
notebook/              # Jupyter notebook for EDA/modeling
utils/                 # Inference and utility scripts
app/
    app.py             # Main Flask app
    templates/         # HTML templates
    static/            # CSS and JS files
```

## Setup & Run
1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd Flight-Price-Prediction-Project
   ```
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Place your model files (`dt_model.pkl`, `scaler.pkl`, `encoded_columns.pkl`) in the `models/` directory.
5. Run the app:
   ```
   python app/app.py
   ```
6. Open your browser to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Notes
- Do **not** commit model files or sensitive data to public repositories.
- For demo purposes, only a few city pairs are supported.
- You can extend the city list and durations in `app.py` and `columns.json`.

## License
MIT
