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
.logo-container { text-align: center; margin: 15px 0; }
.counter-bar {
    background-color: #FFE6D5;
    display: flex; justify-content: center; align-items: center;
    flex-direction: column; font-weight: bold; color: #FF6600;
    padding: 15px; margin-bottom: 15px; border-radius: 10px;
}
.counter-bar > div:first-child { display: flex; justify-content: center; }
.digit-container { overflow: hidden; height: 60px; width: 40px; margin: 0 3px; }
.digit { font-size: 48px; animation: roll 1.2s ease-in-out forwards; }
@keyframes roll { 0% { transform: translateY(100%);} 100% { transform: translateY(0);} }
.counter-title { font-size: 18px; margin-top: 8px; text-transform: uppercase; }

/* Remove Streamlit default gaps */
[data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}
div[data-testid="stVerticalBlock"] > div {
    margin: 0 !important;
    padding: 0 !important;
}

/* Map container fixed height */
.map-container {
    height: 500px;
    position: relative;
}
.story-overlay {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: white;
    z-index: 10;
    border-radius: 10px;
    padding: 20px;
    overflow-y: auto;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
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
    max-width: 600px;
    border-radius: 8px;
}
.story-text {
    font-size: 16px;
    line-height: 1.6;
    text-align: justify;
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
    "Jerusalem": "On a stormy night in Jerusalem, a horrific car crash left a young man bleeding profusely on a rain-slicked road. Yossi, a veteran UH volunteer, dropped everything when the alert came in. Racing through gridlock on his ambucycle, he reached the scene in under three minutes. Every second counted. Pulling out his trauma kit, Yossi applied a tourniquet that stopped the bleeding and stabilized the patient. By the time paramedics arrived, vitals were steady. Doctors later said Yossi’s speed and skill prevented certain death. This rescue, like thousands each year, is possible only because people like you keep UH volunteers equipped and ready 24/7.",
    "Tel Aviv": "In the heart of Tel Aviv during evening rush hour, chaos erupted when a pedestrian was struck by a speeding car. Traffic froze, but United Hatzalah volunteers didn’t hesitate. Cutting through gridlock on ambucycles, they reached the patient in minutes. Oxygen, spinal stabilization, and quick wound management kept him alive as crowds gathered. The hospital team confirmed: early intervention saved this man’s life. When you support UH, you give these medics the tools they need to defy time and traffic every single day.",
    "Haifa": "A Haifa park turned into a nightmare when a toddler began choking on a grape. His mother’s screams pierced the air, and panic spread among bystanders. Two UH medics, just blocks away, raced to the scene. With practiced precision, they cleared the airway and delivered back blows that brought life back to the child. Tears flowed as the little boy began breathing again. These miracles aren’t luck—they’re the result of rapid response and your unwavering support.",
    "Beersheba": "When a 58-year-old man collapsed in his home in Beersheba, his wife dialed for help in tears. UH volunteers were on scene in moments, performing CPR and delivering an electric shock with a defibrillator. His heart started again. Minutes later, he was stable enough for hospital transfer. Today, that man is alive because UH medics refuse to waste a single second—and because donors like you keep life-saving tools in their hands.",
    "Netanya": "A sunny beach day nearly ended in tragedy when a swimmer was pulled from the waves unconscious. UH responders sprinted across the sand, initiating advanced airway management and oxygen delivery right on the shoreline. Slowly, the man regained consciousness. Cheers erupted as he opened his eyes. These victories are the reason UH exists—and why your partnership is priceless.",
    "Eilat": "In Eilat’s crystal-blue waters, a diver’s fun dive turned into a nightmare when an allergic reaction sent her into shock. UH medics were alerted and arrived within minutes, administering epinephrine and stabilizing her until an ambulance arrived. From sea rescues to city streets, UH volunteers are always ready—thanks to you."
}

image_url = "https://israelrescue.org/app/uploads/2022/11/volunteer-1-1024x683.jpg"

# -----------------------
# FUNCTION TO CREATE SNIPPETS
# -----------------------
def create_snippet(text, words=15):
    return " ".join(text.split()[:words]) + "..."

# -----------------------
# MAP + PIE CHART
# -----------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3 style='margin-bottom:10px;'>📍 Live Heatmap & Stories</h3>", unsafe_allow_html=True)
    st.markdown("<div class='map-container'>", unsafe_allow_html=True)

    if st.session_state.selected_story is None:
        # Create map
        m = folium.Map(location=[31.5, 34.8], zoom_start=7, tiles="cartodbpositron")
        HeatMap(list(coordinates.values()), gradient={0.2: '#FFDAB3', 0.4: '#FF944D', 0.6: '#FF6600', 1: '#CC5200'}).add_to(m)

        # Add markers with snippet popups
        for city, coords in coordinates.items():
            snippet = create_snippet(stories[city])
            folium.Marker(
                coords,
                popup=f"<b>{city}</b><br>{snippet}",
                icon=folium.Icon(color="orange", icon="info-sign")
            ).add_to(m)

        map_data = st_folium(m, width=700, height=500)
        if map_data and map_data.get("last_object_clicked"):
            clicked_coords = map_data["last_object_clicked"]
            for city, coords in coordinates.items():
                if abs(coords[0] - clicked_coords["lat"]) < 0.05 and abs(coords[1] - clicked_coords["lng"]) < 0.05:
                    st.session_state.selected_story = city
                    st.experimental_rerun()
    else:
        # Show full story overlay
        city = st.session_state.selected_story
        st.markdown(f"""
        <div class='story-overlay'>
            <form action="" method="post">
                <button class='close-button' name="close">X</button>
            </form>
            <h3>{city}: Featured Rescue</h3>
            <img src='{image_url}' class='story-image'>
            <p class='story-text'>{stories[city]}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Close Story"):
            st.session_state.selected_story = None
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='margin-bottom:10px;'>📊 Call Type Breakdown</h3>", unsafe_allow_html=True)
    fig_pie = px.pie(values=[42, 38, 31, 27, 19], names=["Trauma", "Cardiac", "OB/GYN", "Medical", "Other"],
                     color_discrete_sequence=['#FF6600','#FF944D','#FFDAB3','#FFB380'])
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# BAR CHART BELOW
# -----------------------
st.markdown("<h3 style='margin-bottom:10px;'>🏙️ Top 5 Cities by Call Volume</h3>", unsafe_allow_html=True)
df_cities = pd.DataFrame({"City": list(coordinates.keys()), "Count": [42, 38, 31, 27, 24, 19]})
fig_bar = px.bar(df_cities.head(5), x="Count", y="City", orientation="h", color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)
