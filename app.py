import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium
import streamlit.components.v1 as components

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
    flex-direction: column; font-weight: bold; color: #FF6600; padding: 15px; margin-bottom: 15px; border-radius: 10px;
}
.counter-bar > div:first-child { display: flex; justify-content: center; }
.digit-container { overflow: hidden; height: 60px; width: 40px; margin: 0 3px; }
.digit { font-size: 48px; animation: roll 1.2s ease-in-out forwards; }
@keyframes roll { 0% { transform: translateY(100%);} 100% { transform: translateY(0);} }
.counter-title { font-size: 18px; margin-top: 8px; text-transform: uppercase; }
[data-testid="stHorizontalBlock"] { gap: 1rem !important; }
[data-testid="stPlotlyChart"] { margin-top: 0 !important; padding-top: 0 !important; }
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
# DATA
# -----------------------
data = {
    "City": ["Jerusalem", "Tel Aviv", "Haifa", "Beersheba", "Netanya", "Eilat"],
    "Lat": [31.7683, 32.0853, 32.7940, 31.2520, 32.3215, 29.5577],
    "Lon": [35.2137, 34.7818, 34.9896, 34.7915, 34.8532, 34.9519],
    "Call Type": ["Trauma", "Cardiac", "OB/GYN", "Medical", "Trauma", "Other"],
    "Story": [
        "Volunteer Yossi applied a tourniquet to save a man after a severe car accident on a rainy night in Jerusalem. Thanks to rapid action, the patient survived with stabilized vitals before ambulance arrival.",
        "Medics rushed during rush hour in Tel Aviv to help a pedestrian hit by a car. Their rapid intervention with oxygen and immobilization prevented severe complications and saved the patient's life.",
        "A toddler choked in Haifa park; UH responders cleared the airway and performed life-saving measures in seconds. Their quick action turned a potential tragedy into a miraculous rescue.",
        "Beersheba saw a dramatic rescue after a sudden cardiac arrest. UH volunteers deployed a defibrillator and restarted the man’s heart before paramedics arrived.",
        "A Netanya beach day turned critical when a swimmer was pulled unconscious from the waves. UH responders revived him using advanced airway techniques and oxygen.",
        "In Eilat, a tourist suffered an allergic reaction while diving. UH medics administered epinephrine on the spot, saving her life."
    ]
}
df = pd.DataFrame(data)

# -----------------------
# MAP + PIE CHART SIDE-BY-SIDE
# -----------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<h3 style='margin-bottom:0;'>📍 Live Map of Calls</h3>", unsafe_allow_html=True)
    m = folium.Map(location=[31.5, 34.8], zoom_start=7, tiles="cartodbpositron")
    for i, row in df.iterrows():
        short_story = " ".join(row["Story"].split()[:15]) + "..."
        anchor_id = row["City"].lower().replace(" ", "-")
        popup_html = f"""
        <div style="font-size:14px;">
        <b>{row['City']}</b><br>
        {short_story}<br>
        <a href="#" onclick="scrollToStory('{anchor_id}')" style="color:#FF6600; text-decoration:underline;">Read full story</a>
        </div>
        """
        folium.Marker([row["Lat"], row["Lon"]],
                      popup=popup_html,
                      icon=folium.Icon(color="orange", icon="info-sign")).add_to(m)
    st_folium(m, width=700, height=500)

with col2:
    st.markdown("<h3 style='margin-bottom:0;'>📊 Call Type Breakdown</h3>", unsafe_allow_html=True)
    fig_pie = px.pie(df, names="Call Type",
                     color_discrete_sequence=['#FF6600','#FF944D','#FFDAB3','#FFB380'])
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# TOP CITIES (TOP 5 ONLY)
# -----------------------
st.markdown("<h3 style='margin-bottom:0;'>🏙️ Top 5 Cities by Call Volume</h3>", unsafe_allow_html=True)
city_counts = df["City"].value_counts().reset_index().head(5)
city_counts.columns = ["City", "Count"]
fig_bar = px.bar(city_counts, x="Count", y="City", orientation='h', color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------
# STORIES SECTION (150 WORDS EACH)
# -----------------------
st.markdown("<h3 id='top-stories'>📖 Top Stories</h3>", unsafe_allow_html=True)
image_url = "https://israelrescue.org/app/uploads/2022/11/volunteer-1-1024x683.jpg"
stories = [
    {
        "id": "jerusalem",
        "title": "Jerusalem: A Tourniquet Saves a Life",
        "text": "On a stormy night in Jerusalem, a driver lost control and slammed into a guardrail. Yossi, a seasoned UH volunteer, dropped everything and sped to the scene. Arriving in under three minutes, he found a young man bleeding profusely from a severed artery. Every second mattered. Yossi grabbed his trauma kit, applied a tourniquet, and stopped the bleeding before the victim lost consciousness. His calm precision in chaos kept the patient alive until an ambulance took over. Doctors later confirmed: without Yossi’s intervention, the man would have died. This is why speed matters—and why your support makes lifesaving possible."
    },
    {
        "id": "tel-aviv",
        "title": "Tel Aviv: Rush Hour Heroics",
        "text": "Traffic stood still as panic spread across Tel Aviv. A pedestrian had been struck in the heart of the city’s busiest district. Within moments, UH volunteers arrived, cutting through the congestion on ambucycles. They stabilized the victim’s airway, provided oxygen, and secured a spinal board, all while horns blared and crowds gathered. Their rapid response prevented paralysis and kept the patient breathing en route to Ichilov Hospital. This wasn’t just a rescue—it was a race against time that ended in victory thanks to speed, training, and your generosity powering every second."
    },
    {
        "id": "haifa",
        "title": "Haifa: Toddler’s Choking Emergency",
        "text": "In a Haifa park, a carefree afternoon turned terrifying. A toddler choked on a grape, his tiny face turning blue as his mother screamed for help. Two UH volunteers, nearby and alert, sprinted toward the cries. They executed back blows and cleared the airway in seconds, reviving the child before the ambulance even arrived. The mother collapsed into tears of relief, clutching her breathing child to her chest. Today, that child is laughing and alive—all because of the relentless dedication of UH medics and donors like you who keep them ready for moments like this."
    }
]
for story in stories:
    st.markdown(f'<div id="story-{story["id"]}"></div>', unsafe_allow_html=True)
    with st.expander(story["title"], expanded=False):
        st.image(image_url, use_container_width=True)
        st.write(story["text"])

# -----------------------
# JS FOR SMOOTH SCROLL
# -----------------------
components.html("""
<script>
function scrollToStory(storyId){
    const el = parent.document.querySelector('#story-' + storyId);
    if(el){ el.scrollIntoView({behavior: 'smooth', block: 'start'}); }
}
</script>
""", height=0)
