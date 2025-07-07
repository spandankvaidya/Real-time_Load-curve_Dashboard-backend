import lightgbm as lgb
import polars as pl
import numpy as np
from dateutil import parser
from app import globals

model = lgb.Booster(model_file="lightgbm_power_model_2.txt")

def transform_datetime_column(pl_df):
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

def load_and_predict(date):
    from pathlib import Path
    import pandas as pd

    file_path = f"data/{date}.csv"
    if not Path(file_path).exists():
        return False

    df = pd.read_csv(file_path)
    globals.predicted_values.clear()
    globals.actual_values.clear()
    globals.timestamps.clear()
    globals.selected_date = date

    for _, row in df.iterrows():
        features = {
            'Datetime': row['Datetime'],
            'Temperature': row['Temperature'],
            'Humidity': row['Humidity'],
            'WindSpeed': row['WindSpeed'],
            'GeneralDiffuseFlows': row['GeneralDiffuseFlows'],
            'DiffuseFlows': row['DiffuseFlows']
        }
        actual = row['POWER']

        pl_df = pl.DataFrame([features])
        pl_df, dt_objects = transform_datetime_column(pl_df)

        X = pl_df.to_pandas()
        X = X[[  # Ensure correct feature order
            'Month_sin', 'Month_cos', 'Time_sin', 'Time_cos',
            'Temperature', 'Humidity', 'WindSpeed',
            'GeneralDiffuseFlows', 'DiffuseFlows'
        ]]

        prediction = model.predict(X)[0]
        time_str = dt_objects[0].strftime("%H:%M")

        globals.predicted_values.append(prediction)
        globals.actual_values.append(actual)
        globals.timestamps.append(time_str)

    return True
