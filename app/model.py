# In app/model.py

import lightgbm as lgb
import polars as pl
import numpy as np
from dateutil import parser
import os
from pathlib import Path

# Load model only once when the module is imported
model_path = os.path.join(os.path.dirname(__file__), "lightgbm_power_model_2.txt")
model = lgb.Booster(model_file=model_path)


def transform_datetime_features(pl_df):
    # This function is fine, just renaming for clarity
    # ... (no changes needed inside this function, I'm just copying it here for completeness)
    dt_series = pl_df['Datetime'].to_list()
    dt_objects = [parser.parse(dt) for dt in dt_series]

    months = [dt.month for dt in dt_objects]
    minutes = [dt.hour * 60 + dt.minute for dt in dt_objects]

    month_sin = [np.sin(2 * np.pi * m / 12) for m in months]
    month_cos = [np.cos(2 * np.pi * m / 12) for m in months]
    time_sin = [np.sin(2 * np.pi * t / 1440) for t in minutes]
    time_cos = [np.cos(2 * np.pi * t / 1440) for t in minutes]

    pl_df = pl_df.with_columns([
        pl.Series('Month_sin', month_sin),
        pl.Series('Month_cos', month_cos),
        pl.Series('Time_sin', time_sin),
        pl.Series('Time_cos', time_cos)
    ])

    return pl_df.drop("Datetime"), dt_objects


def run_prediction_for_date(date: str):
    # CORRECTED FILE PATH LOGIC
    # Assumes your data is in `app/test/` relative to the project root
    file_path = Path(__file__).parent / "test" / f"{date}.csv"
    
    if not file_path.exists():
        print(f"Error: Data file not found at {file_path}")
        return None # Return None if file not found

    # Using polars for faster CSV reading
    df = pl.read_csv(file_path)

    # Transform features and get datetime objects
    features_df, dt_objects = transform_datetime_features(df.clone())
    
    # Select features for prediction in the correct order
    X = features_df.select([
        'Month_sin', 'Month_cos', 'Time_sin', 'Time_cos',
        'Temperature', 'Humidity', 'WindSpeed',
        'GeneralDiffuseFlows', 'DiffuseFlows'
    ]).to_pandas()

    # Get predictions
    predictions = model.predict(X)

    # Prepare results
    results = {
        "timestamps": [dt.strftime("%H:%M") for dt in dt_objects],
        "predicted_values": predictions.tolist(),
        "actual_values": df['POWER'].to_list()
    }
    
    return results
