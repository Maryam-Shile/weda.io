def run_forecast(data, months, freq="MS"):
    """
    Run rainfall forecast using StatsForecast AutoARIMA
    """
    import pandas as pd
    import numpy as np
    from statsforecast.models import AutoARIMA
    from statsforecast import StatsForecast

    # Date handling
    data['date'] = pd.to_datetime(data['date'])

    # Variance-stabilizing transform
    data['logged_tp'] = np.sqrt(data['tp'])

    # Prepare StatsForecast format
    rain_train = data[['date', 'logged_tp']].copy()
    rain_train['unique_id'] = 'weather'

    rain_train = rain_train.rename(columns={
        'date': 'ds',
        'logged_tp': 'y'
    })

    rain_train = rain_train.sort_values(['unique_id', 'ds'])

    # Model
    model = AutoARIMA(season_length=12, alias='SARIMA')
    sf = StatsForecast(models=[model], freq=freq)

    sf.fit(rain_train)
    pred = sf.predict(h=months)

    # Inverse transform
    pred['SARIMA'] = pred['SARIMA'] ** 2

    return pred['SARIMA']


def temp_forecast(data, months, freq="MS"):
    """
    Run temperature forecast using StatsForecast AutoARIMA
    """
    import pandas as pd
    from statsforecast.models import AutoARIMA
    from statsforecast import StatsForecast

    data = data.copy()
    data["date"] = pd.to_datetime(data["date"])

    temp_train = data[["date", "t2m"]].copy()
    temp_train["unique_id"] = "temp_series"

    temp_train = temp_train.rename(
        columns={
            "date": "ds",
            "t2m": "y"
        }
    )

    temp_train = temp_train.sort_values(["unique_id", "ds"])

    model = AutoARIMA(season_length=12, alias="SARIMA")
    sf = StatsForecast(models=[model], freq=freq)

    sf.fit(temp_train)
    pred = sf.predict(h=months)

    return pred["SARIMA"]

def get_crop_data(df, Crop):
    import pandas as pd
    return df[df['Crop'] == Crop]
        



def interpret_with_llm(crop_row, prediction_rain, prediction_temp):
    import requests
    import streamlit as st
    import numpy as np
    api_key = st.secrets['OPENROUTER_API_KEY']

    # Extract crop data
    crop_name = crop_row["Crop"]
    min_temp = crop_row["Min Temp (°C)"]
    max_temp = crop_row["Max Temp (°C)"]
    min_rain = crop_row["Min Rainfall (mm)"]
    max_rain = crop_row["Max Rainfall (mm)"]
    soil_type = crop_row["Soil Type"]
    soil_ph = crop_row["Soil pH"]

    # Use averages of predictions
    pred_temp = np.mean(prediction_temp)
    pred_rain = np.mean(prediction_rain)

    prompt = f"""
    You are an agricultural consultant with over 20 years of field experience.

    Crop: {crop_name}

    Optimal requirements:
    - Temperature: {min_temp}–{max_temp} °C
    - Rainfall: {min_rain}–{max_rain} mm
    - Soil: {soil_type}, pH {soil_ph}

    Predicted conditions:
    - Average temperature: {pred_temp:.1f} °C
    - Expected rainfall: {pred_rain:.1f} mm

    Provide a concise advisory (2–3 sentences) on crop suitability, risks, and recommendations.
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek/deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 120,
            "temperature": 0.3
        }
    )

    return response.json()["choices"][0]["message"]["content"]

def plot_result(rain_pred, temp_pred, period):
    import pandas as pd
    df = pd.DataFrame(
        {
            "Rain": rain_pred,
            "Temperature": temp_pred,
            "Period": pd.date_range(start = '2026-01-01', periods = period, freq = 'M')
        }
    ).set_index("Period")
    return df


