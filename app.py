import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from utils.sarima import run_forecast, temp_forecast, get_crop_data, plot_result, interpret_with_llm

st.set_page_config(page_title="weda.io", layout="wide")

st.title("Weda - Climate Prediction & Crop Advisory Tool")
st.write("Select a location, year, and crop to get predictions.")

# ---------------- MAP ----------------
st.subheader("Select Location")

m = folium.Map(location=[4.05, 9.7], zoom_start=6)
map_data = st_folium(m, height=400, width=700)

lat, lon = None, None
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

st.write("Latitude:", lat)
st.write("Longitude:", lon)

# ---------------- INPUTS ----------------
st.subheader("Prediction Inputs")

month = st.selectbox("Prediction Steps (months)", [1, 3, 6, 12, 15, 18, 24])
crop = st.selectbox(
    "Crop",
    ['Maize', 'Rice (lowland)', 'Rice (upland)', 'Sorghum', 'Soybean', 'Cassava', 'Sugar Cane']
)

# ---------------- DATA SOURCE ----------------
@st.cache_data
def fetch_weather_data(lat, lon):
    url_1 = "https://raw.githubusercontent.com/Maryam-Shile/weda.io/main/utils/data/Temperature/era_5_2000_2026.csv" 
    return pd.read_csv(url_1)

@st.cache_data
def get_crop_info():
    url_2 = "https://raw.githubusercontent.com/Maryam-Shile/weda.io/main/utils/data/Makwa%20crop%20data%20-%20Sheet4.csv"
    return pd.read_csv(url_2)

@st.cache_data
def fetch_rain_data():
    url_3 = "https://raw.githubusercontent.com/Maryam-Shile/weda.io/main/utils/data/rainfall_2000_2026.csv"
    return pd.read_csv(url_3)

# ---------------- RUN ----------------
if st.button("Run Prediction"):

    if lat is None or lon is None:
        st.error("Please select a location on the map.")
    else:
        st.info("Fetching data...")
        weather_df = fetch_weather_data(lat, lon)

        crop_info = get_crop_info()

        rain_data = fetch_rain_data()


        st.info("Running predictions...")
        prediction_rain = run_forecast(rain_data, month)
        prediction_temp = temp_forecast(weather_df, month)
        crop_data = get_crop_data(crop_info, crop)


        st.info("A moment please, interpreting results...")
        result = interpret_with_llm(crop_data, prediction_rain, prediction_temp )
        chart_df = plot_result(prediction_rain, prediction_temp, month)

        st.success("Prediction complete!")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Rainfall Prediction')
            st.line_chart(chart_df['Rain'])
            st.metric(f"Average Expected Rainfall (mm) for the next {month} months", f"{chart_df['Rain'].mean():.1f}")

        with col2:
            st.subheader('Temperature Prediction')
            st.line_chart(chart_df['Temperature'])
            st.metric(f"Average Expected Temperature (°C) for the next {month} months", f"{chart_df['Temperature'].mean():.1f}")
            

        st.write("Recommendation")
        st.write(result)
