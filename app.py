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
# CUSTOM CSS FOR LAYOUT FIXES
# -----------------------
st.markdown("""
<style>
/* Sticky orange header */
.header-bar {
    background-color: #FF6600;
    text-align: center;
    padding: 8px 0;  /* Minimal padding */
    color: white;
    font-size: 32px;
    font-weight: bold;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
}

/* Remove Streamlit default top padding */
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Spacer below header */
.header-spacer {
    height: 20px !important;
}

/* Logo container */
.logo-container {
    text-align: center;
    margin: 5px 0 20px 0;
}

/* Counter container */
.counter-bar {
    background-color: #FFE6D5;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    font-weight: bold;
    color: #FF6600;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
}

/* Counter digits in one row */
.counter-bar > div:first-child {
    display: flex;
    justify-content: center;
}

/* Digit container */
.digit-container {
    overflow: hidden;
    height: 60px;
    width: 40px;
    margin: 0 3px;
}
.digit {
    font-size: 48px;
    animation: roll 1.2s ease-in-out forwards;
}
@keyframes roll {
    0% { transform: translateY(100%); }
    100% { transform: translateY(0); }
}

/* Counter title */
.counter-title {
    font-size: 18px;
    margin-top: 8px;
    text-transform: uppercase;
}

/* Tight chart title spacing */
h2, h3, .stSubheader {
    margin-bottom: 2px !important;
    margin-top: 8px !important;
}

/* Remove extra padding above Plotly charts */
[data-testid="stPlotlyChart"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown("<div class='header-bar'>YOUR DAY OF LIFESAVING</div>", unsafe_allow_html=True)
st.markdown("<div class='header-spacer'></div>", unsafe_allow_html=True)

# -----------------------
# LOGO
# -----------------------
st.markdown("<div class='logo-container'>"
            "<img src='https://israelrescue.org/app/uploads/2023/08/UH-logo.svg' width='200'>"
            "</div>", unsafe_allow_html=True)

# -----------------------
# COUNTER
# -----------------------
number = "1248"
digits_html = "".join([f"""
<div class='digit-container'>
    <div class='digit'>{d}</div>
</div>""" for d in number])

st.markdown(f"""
<div class='counter-bar'>
    <div>{digits_html}</div>
    <div class='counter-title'>Calls and counting!</div>
</div>
""", unsafe_allow_html=True)

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
# MAP & CHARTS
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
