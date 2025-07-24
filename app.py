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
.header-bar {
    background-color: #FF6600;
    text-align: center;
    padding: 8px 0;
    color: white;
    font-size: 32px;
    font-weight: bold;
    position: fixed;
    top: 0; left: 0;
    width: 100%;
    z-index: 100;
}
.block-container { padding-top: 0 !important; margin-top: 0 !important; }
.header-spacer { height: 20px !important; }
.logo-container { text-align: center; margin: 5px 0 10px 0; }
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
# MAP + PIE CHART (SIDE BY SIDE)
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
        <a href="#story-{anchor_id}" onclick="scrollToStory('{anchor_id}')" style="color:#FF6600; text-decoration:underline;">Read full story</a>
        </div>
        """
        folium.Marker([row["Lat"], row["Lon"]],
                      popup=popup_html,
                      icon=folium.Icon(color="orange", icon="info-sign")).add_to(m)
    st_folium(m, width=700, height=500)

with col2:
    st.markdown("<h3 style='margin-bottom:0;'>📊 Call Type Breakdown</h3>", unsafe_allow_html=True)
    fig_pie = px.pie(df, names="Call Type",
                     color_discrete_sequence=['#FF6600','#FF944D','#FFDAB3'])
    fig_pie.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------
# BAR CHART
# -----------------------
st.markdown("<h3 style='margin-bottom:0;'>🏙️ Top Cities by Call Volume</h3>", unsafe_allow_html=True)
city_counts = df["City"].value_counts().reset_index()
city_counts.columns = ["City", "Count"]
fig_bar = px.bar(city_counts, x="Count", y="City", orientation='h', color_discrete_sequence=['#FF6600'])
fig_bar.update_layout(showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------
# STORIES SECTION
# -----------------------
st.markdown("<h3 id='top-stories'>📖 Top Stories</h3>", unsafe_allow_html=True)
stories = [
    {
        "id": "jerusalem",
        "title": "Jerusalem: Tourniquet Saves a Life",
        "image": "https://images.unsplash.com/photo-1582719478178-9a4b91d70b7e",
        "text": "On a cold, rainy night in Jerusalem, a major accident left a man critically injured and bleeding heavily. Within seconds of receiving the alert, volunteer Yossi raced through traffic, reaching the scene in just under three minutes. He quickly assessed the patient, applied a life-saving tourniquet, and managed to stabilize vital signs until advanced teams arrived. Doctors later confirmed that his quick action prevented certain death. This dramatic rescue highlights the impact of speed, training, and your support."
    },
    {
        "id": "tel-aviv",
        "title": "Tel Aviv: Rush Hour Heroics",
        "image": "https://images.unsplash.com/photo-1556742044-3c52d6e88c62",
        "text": "In Tel Aviv’s busiest district, a pedestrian lay motionless after being hit by a car. Amid chaos, UH medics pushed through traffic to reach the victim within minutes. They provided oxygen, immobilized the spine, and treated injuries right on the asphalt. This intervention prevented life-threatening complications and bought precious time before hospital transfer. The patient survived surgery and is now recovering, thanks to swift teamwork and unwavering commitment to saving lives."
    },
    {
        "id": "haifa",
        "title": "Haifa: Toddler Choking Emergency",
        "image": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528",
        "text": "Panic gripped a Haifa playground when a toddler choked on food. Parents screamed as seconds ticked away. Two UH volunteers, stationed nearby, sprinted to the scene. They delivered back blows and airway clearing techniques that restored the child’s breathing just as the ambulance arrived. The mother broke down in tears, clutching her child, overcome with relief. For this family, UH volunteers were angels in orange, turning terror into hope."
    }
]
for story in stories:
    st.markdown(f'<a name="story-{story["id"]}"></a>', unsafe_allow_html=True)
    with st.expander(story["title"], expanded=False):
        st.image(story["image"], use_container_width=True)
        st.write(story["text"])

# -----------------------
# JS FOR SMOOTH SCROLL
# -----------------------
components.html("""
<script>
function scrollToStory(storyId){
    const el = document.querySelector('[name="story-' + storyId + '"]');
    if(el){ el.scrollIntoView({behavior: 'smooth', block: 'start'}); }
}
</script>
""", height=0)
