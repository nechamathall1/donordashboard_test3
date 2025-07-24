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
# CUSTOM CSS
# -----------------------
st.markdown("""
<style>
/* Sticky header */
.header-bar {
    background-color: #FF6600;
    text-align: center;
    padding: 8px 0;
    color: white;
    font-size: 32px;
    font-weight: bold;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 100;
}
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
/* Spacer below header */
.header-spacer { height: 20px !important; }
/* Logo */
.logo-container { text-align: center; margin: 5px 0 15px 0; }
/* Counter */
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
/* Remove gaps between charts and sections */
[data-testid="stHorizontalBlock"] { gap: 1rem !important; }
[data-testid="stVerticalBlock"] { margin-bottom: 0 !important; }
/* Tight chart title spacing */
h2, h3, .stSubheader { margin-bottom: 2px !important; }
[data-testid="stPlotlyChart"] { margin-top: 0 !important; padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown("<div class='header-bar'>UNITED HATZALAH REAL-TIME DASHBOARD</div>", unsafe_allow_html=True)
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
# DATA
# -----------------------
data = {
    "City": ["Jerusalem", "Tel Aviv", "Haifa"],
    "Lat": [31.7683, 32.0853, 32.7940],
    "Lon": [35.2137, 34.7818, 34.9896],
    "Call Type": ["Trauma", "Cardiac", "OB/GYN"],
    "Story": [
        "Volunteer Yossi applied a tourniquet to save a man after a severe car accident on a rainy night in Jerusalem. Thanks to rapid action, the patient survived with stabilized vitals before ambulance arrival.",
        "Medics rushed during rush hour in Tel Aviv to help a pedestrian hit by a car. Their rapid intervention with oxygen and immobilization prevented severe complications and saved the patient's life.",
        "A toddler choked in Haifa park; UH responders cleared the airway and performed life-saving measures in seconds. Their quick action turned a potential tragedy into a miraculous rescue."
    ]
}
df = pd.DataFrame(data)

# -----------------------
# MAP
# -----------------------
st.markdown("<h3 style='margin-bottom:0;'>📍 Live Map of Calls</h3>", unsafe_allow_html=True)
m = folium.Map(location=[31.5, 34.8], zoom_start=7, tiles="cartodbpositron")
for i, row in df.iterrows():
    anchor_id = row["City"].lower().replace(" ", "-")
    short_story = " ".join(row["Story"].split()[:15]) + "..."
    popup_html = f"""
    <div style="font-size:14px;">
    <b>{row['City']}</b><br>
    {short_story}<br>
    <a href="#story-{anchor_id}" onclick="scrollToStory('{anchor_id}')" style="color:#FF6600; text-decoration:underline;">Read full story</a>
    </div>
    """
    folium.Marker(
        location=[row["Lat"], row["Lon"]],
        popup=popup_html,
        icon=folium.Icon(color="orange", icon="info-sign")
    ).add_to(m)
st_folium(m, width=700, height=500)

# -----------------------
# PIE CHART
# -----------------------
st.subheader("📊 Call Type Breakdown")
fig_pie = px.pie(df, names="Call Type",
                 color_discrete_sequence=['#FF6600','#FF944D','#FFDAB3'])
fig_pie.update_traces(textinfo="percent+label")
st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# BAR CHART (ZERO GAP)
# -----------------------
st.markdown("<h3 style='margin-bottom:0;'>🏙️ Top Cities by Call Volume</h3>", unsafe_allow_html=True)
city_counts = df["City"].value_counts().reset_index()
city_counts.columns = ["City", "Count"]
fig_bar = px.bar(city_counts, x="Count", y="City", orientation='h',
                 color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------
# TOP STORIES
# -----------------------
st.markdown("<h3 id='top-stories'>📖 Top Stories</h3>", unsafe_allow_html=True)
stories = [
    {
        "id": "jerusalem",
        "title": "Jerusalem: Tourniquet Saves a Life",
        "image": "https://images.unsplash.com/photo-1603902853190-7d8f3b307b19",
        "text": "On a rainy night in Jerusalem, UH volunteer Yossi raced through traffic after receiving an urgent alert. A man lay critically injured from a car crash, bleeding heavily. Within moments, Yossi applied a tourniquet and stopped the bleeding. He monitored vitals until an ambulance arrived. Doctors later confirmed that his intervention saved the man's life. Quick, professional, and selfless—this is what makes UH volunteers heroes every day."
    },
    {
        "id": "tel-aviv",
        "title": "Tel Aviv: Pedestrian Rescued",
        "image": "https://images.unsplash.com/photo-1549575810-750b0fc78e5d",
        "text": "In Tel Aviv’s bustling center, a pedestrian was struck by a car during rush hour. United Hatzalah medics arrived in under 3 minutes, stabilizing the patient with oxygen and spinal immobilization. Their timely efforts prevented catastrophic complications. Today, that patient is recovering in the hospital because volunteers dropped everything to answer the call."
    },
    {
        "id": "haifa",
        "title": "Haifa: Child Choking Emergency",
        "image": "https://images.unsplash.com/photo-1587825140708-62f96e6d90b1",
        "text": "Panic spread through a Haifa park as a toddler choked on food. In seconds, UH responders sprinted to the scene. They used back blows and suction to clear the airway, saving the child’s life. The mother wept with gratitude as her child began breathing normally. Another tragedy prevented—thanks to you and the UH family."
    }
]
for story in stories:
    st.markdown(f'<a name="story-{story["id"]}"></a>', unsafe_allow_html=True)
    with st.expander(story["title"], expanded=False):
        st.image(story["image"], use_container_width=True)
        st.write(story["text"])

# -----------------------
# JAVASCRIPT FOR AUTO SCROLL (WORKAROUND)
# -----------------------
components.html("""
<script>
function scrollToStory(storyId){
    const el = document.querySelector('[name="story-' + storyId + '"]');
    if(el){
        el.scrollIntoView({behavior: 'smooth'});
    }
}
</script>
""", height=0)
