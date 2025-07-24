import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium
import random
import time

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="United Hatzalah Dashboard", layout="wide")

# -----------------------
# CSS STYLING
# -----------------------
st.markdown("""
<style>
.header-bar {
    background:#FF6600;
    color:white;
    text-align:center;
    padding:10px;
    font-size:32px;
    font-weight:bold;
}
.header-spacer {height:60px;}
.counter-bar {
    background:#FFE6D5;
    color:#FF6600;
    font-weight:bold;
    text-align:center;
    padding:15px;
    border-radius:10px;
    height:120px;
}
.story-box {
    background:#FFF3E6;
    border-left:8px solid #FF6600;
    padding:15px;
    margin-top:20px;
    border-radius:10px;
}
.story-title {
    color:#FF6600;
    font-size:20px;
    font-weight:bold;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown("<div class='header-bar'>UNITED HATZALAH REAL-TIME DASHBOARD</div>", unsafe_allow_html=True)
st.markdown("<div class='header-spacer'></div>", unsafe_allow_html=True)
st.image("https://israelrescue.org/app/uploads/2023/08/UH-logo.svg", width=200)

# -----------------------
# PLACEHOLDERS
# -----------------------
counter_placeholder = st.empty()
col1, col2 = st.columns([2, 1])
with col1:
    map_placeholder = st.empty()
with col2:
    pie_placeholder = st.empty()
bar_placeholder = st.empty()
story_placeholder = st.empty()

# -----------------------
# AUTO-REFRESH CONTROL
# -----------------------
refresh_interval = 10  # seconds
stop_refresh = st.checkbox("Pause Auto-Refresh", value=False)

# -----------------------
# MAP BUILDER FUNCTION
# -----------------------
def build_map(data):
    m = folium.Map(location=[31.8, 35.1], zoom_start=8)
    heat_data = [[row["lat"], row["lon"], row["calls"]] for _, row in data.iterrows()]
    HeatMap(heat_data, radius=25, gradient={0.2: 'yellow', 0.6: 'orange', 1: 'red'}).add_to(m)
    for _, row in data.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=f"{row['city']}: {row['calls']} calls",
            popup=row["story"]
        ).add_to(m)
    return m

# -----------------------
# LIVE UPDATE LOOP
# -----------------------
while not stop_refresh:
    # Simulate dynamic data retrieval
    call_count = 1248 + random.randint(0, 20)
    data = pd.DataFrame({
        "lat": [31.78, 32.08, 32.17, 31.25, 32.09],
        "lon": [35.22, 34.78, 34.85, 34.79, 34.80],
        "city": ["Jerusalem", "Tel Aviv", "Netanya", "Ashdod", "Herzliya"],
        "calls": [random.randint(50, 200) for _ in range(5)],
        "story": [
            "Volunteer raced to save a man who collapsed during prayers in Jerusalem.",
            "In Tel Aviv, a motorcyclist was revived after a severe accident.",
            "A child was choking in Netanya—saved in minutes by UH medics.",
            "Cardiac arrest in Ashdod—rescue team arrived in under 3 minutes.",
            "
