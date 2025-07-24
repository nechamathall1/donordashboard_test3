import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

# -----------------------
# PAGE CONFIGURATION
# -----------------------
st.set_page_config(page_title="United Hatzalah Dashboard", layout="wide")

# -----------------------
# CUSTOM CSS STYLING
# -----------------------
st.markdown("""
    <style>
    .main {background-color: #F9F9F9;}
    .header-bar {
        background-color: #FF6600;
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 36px;
        font-weight: bold;
    }
    .logo {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: -20px;
    }
    .logo img {
        height: 70px;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER WITH LOGO & TITLE
# -----------------------
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("UH-logo.svg", use_column_width=False, width=120)
with col_title:
    st.markdown("<h2 style='color:#FF6600; font-weight:bold;'>UNITED HATZALAH</h2>", unsafe_allow_html=True)

# ORANGE HEADER BAR
st.markdown("<div class='header-bar'>CALLS TODAY: 1,248 AND COUNTING...</div>", unsafe_allow_html=True)

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
# LAYOUT: MAP + CHARTS
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
    st.subheader("📊 Distribution of Call Types")
    fig_pie = px.pie(df, names="Call Type", title="", color_discrete_sequence=['#FF6600','#FF944D','#FFDAB3','#FFB380'])
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# TOP CITIES
# -----------------------
st.subheader("🏙️ Top Cities by Call Volume")
city_counts = df["City"].value_counts().reset_index()
city_counts.columns = ["City", "Count"]
fig_bar = px.bar(city_counts, x="Count", y="City", orientation='h', color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)