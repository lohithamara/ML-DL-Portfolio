
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow INFO and WARNING
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN custom ops info
import numpy as np
import pandas as pd
import joblib

def load_artifacts():
    base_path = os.path.dirname(os.path.abspath(__file__))
    model = joblib.load(os.path.join(base_path, '../models/ann_model.pkl'))
    scaler = joblib.load(os.path.join(base_path, '../models/scaler.pkl'))
    encoded_columns = joblib.load(os.path.join(base_path, '../models/encoded_columns.pkl'))
    # If encoded_columns is a DataFrame, extract columns as list
    if hasattr(encoded_columns, 'columns'):
        encoded_columns = encoded_columns.columns.tolist()
    return model, scaler, encoded_columns

def preprocess_input(input_dict, scaler, encoded_columns):
    # Numerical columns
    num_cols = ['stops', 'duration', 'days_left']
    num_data = {col: [input_dict.get(col, 0)] for col in num_cols}
    num_df = pd.DataFrame(num_data)
    num_scaled = scaler.transform(num_df)
    # Categorical columns (one-hot)
    cat_data = {col: 0 for col in encoded_columns}
    for key, value in input_dict.items():
        if isinstance(value, str):
            col_name = f"{key}_{value}" if f"{key}_{value}" in encoded_columns else value
            if col_name in cat_data:
                cat_data[col_name] = 1
    # Combine
    final_data = []
    for col in encoded_columns:
        if col in num_cols:
            idx = num_cols.index(col)
            final_data.append(num_scaled[0][idx])
        else:
            final_data.append(cat_data[col])
    # Ensure encoded_columns is a 1D list
    if hasattr(encoded_columns, 'tolist'):
        encoded_columns = encoded_columns.tolist()
    if isinstance(encoded_columns, np.ndarray):
        encoded_columns = list(encoded_columns.flatten())
    # Return as DataFrame with correct columns
    X_df = pd.DataFrame([final_data], columns=encoded_columns)
    return X_df

def predict_price(input_dict):
    model, scaler, encoded_columns = load_artifacts()
    X = preprocess_input(input_dict, scaler, encoded_columns)
    price = model.predict(X)[0]
    return price

# Example usage:
# input_dict = {
#     'stops': 0,
#     'duration': 110,
#     'days_left': 10,
#     'airline': 'Air India',
#     'source_city': 'Mumbai',
#     'departure_time': 'Morning',
#     'arrival_time': 'Evening',
#     'destination_city': 'Delhi',
#     'class': 'Business'
# }
# print(predict_price(input_dict))
