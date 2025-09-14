# Flight Price Prediction Web App

A modern Flask web application for searching and comparing flight prices between major Indian cities. Users can enter journey details, view multiple flight options with realistic durations and prices (predicted by a trained ML model), and filter results by airline, stops, and class.

## Features
- Enter source, destination, journey date, and number of passengers
- Realistic flight durations and times based on city pairs
- Prices predicted by a machine learning model (not random)
- Filters for airline, stops, and class
- Responsive, modern UI with professional styling
- "Modify Search" option for easy re-query

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
