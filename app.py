import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium
import time

# -----------------------
# PAGE CONFIGURATION
# -----------------------
st.set_page_config(page_title="United Hatzalah Dashboard", layout="wide")

# -----------------------
# CSS STYLING FOR STICKY HEADER
# -----------------------
st.markdown("""
    <style>
    .header-bar {
        background-color: #FF6600;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 15px;
        color: white;
        font-size: 32px;
        font-weight: bold;
        gap: 15px;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 100;
    }
    .header-spacer {
        height: 100px; /* Prevent content overlap */
    }
    .header-bar img {
        height: 60px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER WITH LOGO + COUNTER (ANIMATED)
# -----------------------
logo_url = "https://upload.wikimedia.org/wikipedia/commons/f/f7/United_Hatzalah_Logo.png"

calls_placeholder = st.empty()
counter_html = f"""
<div class='header-bar'>
    <img src='{logo_url}' alt='UH Logo'>
    CALLS TODAY: <span id='counter'>0</span> AND COUNTING...
</div>
<div class='header-spacer'></div>
"""
calls_placeholder.markdown(counter_html, unsafe_allow_html=True)

# Animate rolling counter
total_calls = 1248
for i in range(0, total_calls + 1, 50):
    calls_placeholder.markdown(f"""
    <div class='header-bar'>
        <img src='{logo_url}' alt='UH Logo'>
        CALLS TODAY: {i:,} AND COUNTING...
    </div>
    <div class='header-spacer'></div>
    """, unsafe_allow_html=True)
    time.sleep(0.05)

# -----------------------
# SAMPLE DATA
# -----------------------
data = {
    "City": ["Jerusalem", "Tel Aviv", "Haifa", "Beersheba", "Netanya", "Eilat"],
    "Lat": [31.7683, 32.0853, 32.7940, 31.2520, 32.3215, 29.5577],
    "Lon": [35.2137, 34.7818, 34.9896, 34.7915, 34.8532, 34.9519],
    "Call Type": ["Trauma", "Cardiac", "OB/GYN", "Trauma", "Medical", "Other"],
    "Story": [
        "Jerusalem: Volunteer Yossi applied a tourniquet and stopped severe bleeding after a car accident.",
        "Tel Aviv: Medics stabilized a pedestrian struck by a car during rush hour.",
        "Haifa: A toddler choking incident was resolved thanks to quick intervention.",
        "Beersheba: A heart attack victim was revived after rapid CPR and defibrillation.",
        "Netanya: UH volunteers saved a drowning swimmer on the boardwalk.",
        "Eilat: A tourist was treated for an allergic reaction during a dive."
    ]
}
df = pd.DataFrame(data)

# -----------------------
# LAYOUT: MAP + PIE
# -----------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Live Map of Calls")
    m = folium.Map(location=[31.5, 34.8], zoom_start=7, tiles="cartodbpositron")
    for i, row in df.iterrows():
        popup_html = f"""
        <div style="font-size:14px;">
        <b>{row['City']}</b><br>
        {row['Story']}
        </div>
        """
        folium.Marker(
            location=[row["Lat"], row["Lon"]],
            popup=popup_html,
            icon=folium.Icon(color="orange", icon="info-sign")
        ).add_to(m)
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("📊 Call Type Breakdown")
    fig_pie = px.pie(df, names="Call Type",
                     color_discrete_sequence=['#FF6600','#FF944D','#FFDAB3','#FFB380'])
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# TOP CITIES BAR CHART
# -----------------------
st.subheader("🏙️ Top Cities by Call Volume")
city_counts = df["City"].value_counts().reset_index()
city_counts.columns = ["City", "Count"]
fig_bar = px.bar(city_counts, x="Count", y="City", orientation='h',
                 color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)
