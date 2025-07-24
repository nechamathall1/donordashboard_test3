import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium
import random

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="United Hatzalah Dashboard", layout="wide")

# -----------------------
# CSS STYLING
# -----------------------
st.markdown("""
<style>
/* Header Bar */
.header-bar {
    background-color: #FF6600;
    text-align: center;
    padding: 10px 0;
    color: white;
    font-size: 32px;
    font-weight: bold;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
}
.header-spacer { height: 60px !important; }

/* Remove Streamlit padding */
header, .block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Logo */
.logo-container {
    text-align: center;
    margin: 5px 0 !important;
}

/* Counter bar */
.counter-bar {
    background-color: #FFE6D5;
    display: flex; justify-content: center; align-items: center;
    flex-direction: column; font-weight: bold; color: #FF6600;
    padding: 15px; margin-bottom: 20px; border-radius: 10px;
}
.counter-bar > div:first-child { display: flex; justify-content: center; }
.digit-container { overflow: hidden; height: 60px; width: 40px; margin: 0 3px; }
.digit { font-size: 48px; animation: roll 1.2s ease-in-out forwards; }
@keyframes roll { 0% { transform: translateY(100%);} 100% { transform: translateY(0);} }
.counter-title { font-size: 18px; margin-top: 8px; text-transform: uppercase; }

/* Tooltip styling (hover snippet) */
.leaflet-tooltip {
    font-size: 12px !important;
    max-width: 180px !important;
    white-space: normal !important;
    word-wrap: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER & LOGO
# -----------------------
st.markdown("<div class='header-bar'>UNITED HATZALAH REAL-TIME DASHBOARD</div>", unsafe_allow_html=True)
st.markdown("<div class='header-spacer'></div>", unsafe_allow_html=True)
st.markdown("<div class='logo-container'><img src='https://israelrescue.org/app/uploads/2023/08/UH-logo.svg' width='200'></div>", unsafe_allow_html=True)

# -----------------------
# COUNTER
# -----------------------
call_count = 1248 + random.randint(0, 5)  # simulate updates
digits_html = "".join([f"<div class='digit-container'><div class='digit'>{d}</div></div>" for d in str(call_count)])
st.markdown(f"""
<div class='counter-bar'>
    <div>{digits_html}</div>
    <div class='counter-title'>Calls Today</div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# DUMMY DATA
# -----------------------
data = pd.DataFrame({
    "lat": [31.78, 32.08, 32.17, 31.25, 32.09],
    "lon": [35.22, 34.78, 34.85, 34.79, 34.80],
    "city": ["Jerusalem", "Tel Aviv", "Netanya", "Ashdod", "Herzliya"],
    "calls": [random.randint(50, 200) for _ in range(5)],
    "story": [
        "Volunteer raced to save a man who collapsed during prayers in Jerusalem.",
        "In Tel Aviv, a motorcyclist was revived after a serious accident.",
        "A child was choking in Netanya—saved in minutes by UH medics.",
        "Cardiac arrest in Ashdod—rescue team arrived in under 3 minutes.",
        "Herzliya beach swimmer rescued from near-drowning thanks to quick CPR."
    ]
})

# -----------------------
# LAYOUT: MAP + PIE CHART
# -----------------------
col1, col2 = st.columns([2, 1])

with col1:
    m = folium.Map(location=[31.8, 35.1], zoom_start=8)
    heat_data = [[row["lat"], row["lon"], row["calls"]] for _, row in data.iterrows()]
    HeatMap(heat_data, radius=25, gradient={0.2: 'yellow', 0.6: 'orange', 1: 'red'}).add_to(m)

    for idx, row in data.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=f"{row['city']}: {row['calls']} calls",
            popup=row["story"]
        ).add_to(m)

    st_data = st_folium(m, width=700, height=500)

with col2:
    fig = px.pie(
        data, values="calls", names="city",
        title="Calls by City",
        color_discrete_sequence=["#FF6600", "#FF8533", "#FF9966", "#FFB399", "#FFD9CC"]
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# FIXED HEIGHT BAR CHART (Orange Theme)
# -----------------------
st.subheader("Call Volume by City")
max_calls = 220  # fixed max for y-axis
bar_fig = px.bar(
    data, x="city", y="calls", text="calls",
    color_discrete_sequence=["#FF6600"]
)
bar_fig.update_traces(textposition="outside")
bar_fig.update_layout(
    yaxis=dict(range=[0, max_calls]),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#FF6600", size=14),
    showlegend=False
)
st.plotly_chart(bar_fig, use_container_width=True)
