import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium

# -----------------------
# PAGE CONFIGURATION
# -----------------------
st.set_page_config(page_title="United Hatzalah Dashboard", layout="wide")

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>
.header-bar {
    background-color: #FF6600; text-align: center; padding: 8px 0;
    color: white; font-size: 32px; font-weight: bold;
    position: fixed; top: 0; left: 0; width: 100%; z-index: 100;
}
.block-container { padding-top: 0 !important; margin-top: 0 !important; }
.header-spacer { height: 20px !important; }
.logo-container { text-align: center; margin: 5px 0 15px 0; }
.counter-bar {
    background-color: #FFE6D5; display: flex; justify-content: center; align-items: center;
    flex-direction: column; font-weight: bold; color: #FF6600;
    padding: 15px; margin-bottom: 15px; border-radius: 10px;
}
.counter-bar > div:first-child { display: flex; justify-content: center; }
.digit-container { overflow: hidden; height: 60px; width: 40px; margin: 0 3px; }
.digit { font-size: 48px; animation: roll 1.2s ease-in-out forwards; }
@keyframes roll { 0% { transform: translateY(100%);} 100% { transform: translateY(0);} }
.counter-title { font-size: 18px; margin-top: 8px; text-transform: uppercase; }

/* Fix gaps between charts */
[data-testid="stVerticalBlock"] > div { margin-bottom: 0 !important; }
div[data-testid="stPlotlyChart"] { margin: 0 !important; padding: 0 !important; }

/* Center story image with max width */
.story-image {
    display: block;
    margin: 0 auto 15px auto;
    max-width: 600px;
    border-radius: 8px;
}
.story-text {
    font-size: 16px;
    line-height: 1.5;
    text-align: justify;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER + LOGO
# -----------------------
st.markdown("<div class='header-bar'>UNITED HATZALAH REAL-TIME DASHBOARD</div>", unsafe_allow_html=True)
st.markdown("<div class='header-spacer'></div>", unsafe_allow_html=True)
st.markdown("<div class='logo-container'><img src='https://israelrescue.org/app/uploads/2023/08/UH-logo.svg' width='200'></div>", unsafe_allow_html=True)

# -----------------------
# COUNTER
# -----------------------
number = "1248"
digits_html = "".join([f"<div class='digit-container'><div class='digit'>{d}</div></div>" for d in number])
st.markdown(f"<div class='counter-bar'><div>{digits_html}</div><div class='counter-title'>Calls and counting!</div></div>", unsafe_allow_html=True)

# -----------------------
# STATE MANAGEMENT
# -----------------------
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "heatmap"

# -----------------------
# SAMPLE CALL DATA FOR HEATMAP
# -----------------------
call_points = [
    [31.7683, 35.2137], [32.0853, 34.7818], [32.7940, 34.9896],
    [31.2520, 34.7915], [32.3215, 34.8532], [29.5577, 34.9519],
    [31.7, 34.9], [32.0, 35.0], [30.8, 34.6], [32.5, 35.0]
]

# -----------------------
# STORIES DATA
# -----------------------
image_url = "https://israelrescue.org/app/uploads/2022/11/volunteer-1-1024x683.jpg"
stories = {
    "Jerusalem": {
        "title": "Jerusalem: A Tourniquet Saves a Life",
        "text": "On a stormy night in Jerusalem, a horrific car crash left a young man bleeding profusely on a rain-slicked road. Yossi, a veteran UH volunteer, dropped everything when the alert came in. Racing through gridlock on his ambucycle, he reached the scene in just under three minutes. Every second counted. Pulling out his trauma kit, Yossi applied a tourniquet that stopped the bleeding and stabilized the patient. By the time paramedics arrived, vitals were steady. Doctors later said Yossi’s speed and skill prevented certain death. This rescue, like thousands each year, is possible only because people like you keep UH volunteers equipped and ready 24/7.",
    },
    "Tel Aviv": {
        "title": "Tel Aviv: Rush Hour Heroics",
        "text": "In the heart of Tel Aviv during evening rush hour, chaos erupted when a pedestrian was struck by a speeding car. Traffic froze, but United Hatzalah volunteers didn’t hesitate. Cutting through the gridlock on ambucycles, they reached the patient in minutes. Oxygen, spinal stabilization, and quick wound management kept him alive as crowds gathered. The hospital team confirmed: early intervention saved this man’s life. When you support UH, you give these medics the tools they need to defy time and traffic every single day.",
    },
    "Haifa": {
        "title": "Haifa: Toddler’s Choking Emergency",
        "text": "A Haifa park turned into a nightmare when a toddler began choking on a grape. His mother’s screams pierced the air, and panic spread among bystanders. Two UH medics, just blocks away, raced to the scene. With practiced precision, they cleared the airway and delivered back blows that brought life back to the child. Tears flowed as the little boy began breathing again. These miracles aren’t luck—they’re the result of rapid response and your unwavering support.",
    },
    "Beersheba": {
        "title": "Beersheba: A Life Restarted",
        "text": "When a 58-year-old man collapsed in his home in Beersheba, his wife dialed for help in tears. UH volunteers were on scene in moments, performing CPR and delivering an electric shock with a defibrillator. His heart started again. Minutes later, he was stable enough for hospital transfer. Today, that man is alive because UH medics refuse to waste a single second—and because donors like you keep life-saving tools in their hands.",
    },
    "Netanya": {
        "title": "Netanya: From Drowning to Breathing",
        "text": "A sunny beach day nearly ended in tragedy when a swimmer was pulled from the waves unconscious. UH responders sprinted across the sand, initiating advanced airway management and oxygen delivery right on the shoreline. Slowly, the man regained consciousness. Cheers erupted as he opened his eyes. These victories are the reason UH exists—and why your partnership is priceless.",
    },
    "Eilat": {
        "title": "Eilat: Allergy Attack Underwater",
        "text": "In Eilat’s crystal-blue waters, a diver’s fun dive turned into a nightmare when an allergic reaction sent her into shock. UH medics were alerted and arrived within minutes, administering epinephrine and stabilizing her until an ambulance arrived. From sea rescues to city streets, UH volunteers are always ready—thanks to you.",
    }
}

# -----------------------
# DISPLAY MAP OR STORY
# -----------------------
st.markdown("<h3 style='margin-bottom:0;'>📍 Emergency Response Map & Stories</h3>", unsafe_allow_html=True)

if st.session_state.view_mode == "heatmap":
    # Heatmap View
    m = folium.Map(location=[31.5, 34.8], zoom_start=7, tiles="cartodbpositron")
    HeatMap(call_points, gradient={0.2: '#FFDAB3', 0.4: '#FF944D', 0.6: '#FF6600', 1: '#CC5200'}).add_to(m)
    st_folium(m, width=700, height=500)

    # Story Buttons
    st.write("### Featured Rescues")
    cols = st.columns(3)
    city_list = list(stories.keys())
    for i, city in enumerate(city_list):
        if cols[i % 3].button(city, key=f"btn_{city}", use_container_width=True):
            st.session_state.view_mode = f"story_{city}"

else:
    # Story View
    city = st.session_state.view_mode.replace("story_", "")
    story = stories[city]
    st.image(image_url, use_container_width=False, output_format="auto", caption=city, width=600)
    st.markdown(f"### {story['title']}")
    st.markdown(f"<p class='story-text'>{story['text']}</p>", unsafe_allow_html=True)
    if st.button("⬅ Back to Map"):
        st.session_state.view_mode = "heatmap"

# -----------------------
# TOP 5 CITIES BAR CHART (WITH GAP FIX)
# -----------------------
st.markdown("<h3 style='margin-bottom:0;'>🏙️ Top 5 Cities by Call Volume</h3>", unsafe_allow_html=True)
df_cities = pd.DataFrame({"City": city_list, "Count": [42, 38, 31, 27, 24, 19]})
fig_bar = px.bar(df_cities.head(5), x="Count", y="City", orientation="h", color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)
