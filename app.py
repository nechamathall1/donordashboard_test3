import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium

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

/* Columns in one row */
[data-testid="stHorizontalBlock"] > div {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
}

/* Map & Overlay */
.map-container {
    position: relative;
    width: 100%;
    margin: 0;
}
.story-overlay {
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 90%;
    background: white;
    z-index: 20;
    padding: 20px;
    border-radius: 10px;
    overflow-y: auto;
    animation: fadeIn 0.4s ease-in-out;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
.close-button {
    position: absolute;
    top: 10px; right: 10px;
    background: #FF6600;
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 50%;
    width: 35px; height: 35px;
    cursor: pointer;
}
.story-image {
    display: block;
    margin: 0 auto 15px auto;
    max-width: 90%;
    border-radius: 8px;
}
.story-text {
    font-size: 16px;
    line-height: 1.6;
    text-align: justify;
}

/* Tooltip styling (hover snippet) */
.leaflet-tooltip {
    font-size: 12px !important;
    max-width: 200px;
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
number = "1248"
digits_html = "".join([f"<div class='digit-container'><div class='digit'>{d}</div></div>" for d in number])
st.markdown(f"""
<div class='counter-bar'>
    <div>{digits_html}</div>
    <div class='counter-title'>Calls and counting!</div>
</div>
""", unsafe_allow_html=True)

# -----------------------
# SESSION STATE
# -----------------------
if "selected_story" not in st.session_state:
    st.session_state.selected_story = None

# -----------------------
# DATA
# -----------------------
coordinates = {
    "Jerusalem": [31.7683, 35.2137],
    "Tel Aviv": [32.0853, 34.7818],
    "Haifa": [32.7940, 34.9896],
    "Beersheba": [31.2520, 34.7915],
    "Netanya": [32.3215, 34.8532],
    "Eilat": [29.5577, 34.9519]
}

stories = {
    "Jerusalem": "On a stormy night in Jerusalem, a horrific car crash left a young man bleeding profusely on a rain-slicked road...",
    "Tel Aviv": "In the heart of Tel Aviv during evening rush hour, chaos erupted when a pedestrian was struck by a speeding car...",
    "Haifa": "A Haifa park turned into a nightmare when a toddler began choking on a grape...",
    "Beersheba": "When a 58-year-old man collapsed in his home in Beersheba, his wife dialed for help in tears...",
    "Netanya": "A sunny beach day nearly ended in tragedy when a swimmer was pulled from the waves unconscious...",
    "Eilat": "In Eilat’s crystal-blue waters, a diver’s fun dive turned into a nightmare..."
}

full_stories = {
    city: text.replace("...", "") + " This rescue, like thousands each year, is possible only because people like you keep UH volunteers equipped and ready 24/7."
    for city, text in stories.items()
}

image_url = "https://israelrescue.org/app/uploads/2022/11/volunteer-1-1024x683.jpg"

def create_snippet(text, words=10):
    return " ".join(text.split()[:words]) + "..."

# -----------------------
# MAIN CONTENT: MAP & PIE
# -----------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📍 Live Heatmap & Stories")
    if st.session_state.selected_story is None:
        m = folium.Map(location=[31.5, 34.8], zoom_start=7, tiles="cartodbpositron")
        HeatMap(list(coordinates.values()), gradient={0.2: '#FFDAB3', 0.4: '#FF944D', 0.6: '#FF6600', 1: '#CC5200'}).add_to(m)

        for city, coords in coordinates.items():
            snippet = create_snippet(full_stories[city])
            folium.Marker(
                coords,
                tooltip=snippet,  # ✅ Hover snippet
                popup=city,       # Click detection
                icon=folium.Icon(color="orange", icon="info-sign")
            ).add_to(m)

        map_data = st_folium(m, width=700, height=500)
        if map_data and map_data.get("last_object_clicked"):
            clicked_coords = map_data["last_object_clicked"]
            for city, coords in coordinates.items():
                if abs(coords[0] - clicked_coords["lat"]) < 0.05 and abs(coords[1] - clicked_coords["lng"]) < 0.05:
                    st.session_state.selected_story = city
                    st.rerun()
    else:
        city = st.session_state.selected_story
        st.markdown(f"""
        <div class='map-container'>
            <div class='story-overlay'>
                <button class='close-button' onclick="window.parent.postMessage('close','*')">X</button>
                <h3>{city}: Featured Rescue</h3>
                <img src='{image_url}' class='story-image'>
                <p class='story-text'>{full_stories[city]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Close Story"):
            st.session_state.selected_story = None
            st.rerun()

with col2:
    st.markdown("### 📊 Call Type Breakdown")
    fig_pie = px.pie(values=[42, 38, 31, 27, 19], names=["Trauma", "Cardiac", "OB/GYN", "Medical", "Other"],
                     color_discrete_sequence=['#FF6600','#FF944D','#FFDAB3','#FFB380'])
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# BAR CHART BELOW
# -----------------------
st.markdown("### 🏙️ Top 5 Cities by Call Volume")
df_cities = pd.DataFrame({"City": list(coordinates.keys()), "Count": [42, 38, 31, 27, 24, 19]})
fig_bar = px.bar(df_cities.head(5), x="Count", y="City", orientation="h", color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False, margin=dict(l=20,r=20,t=20,b=20))
st.plotly_chart(fig_bar, use_container_width=True)
