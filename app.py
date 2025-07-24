import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import folium
import random
import time

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="United Hatzalah Dashboard", layout="wide")

# -----------------------
# CSS STYLING
# -----------------------
st.markdown("""
<style>
.header-bar {background:#FF6600;color:white;text-align:center;padding:10px;font-size:32px;font-weight:bold;}
.header-spacer {height:60px;}
.counter-bar {background:#FFE6D5;color:#FF6600;font-weight:bold;text-align:center;padding:15px;border-radius:10px;height:120px;}
.story-box {background:#FFF3E6;border-left:8px solid #FF6600;padding:15px;margin-top:20px;border-radius:10px;}
.story-title {color:#FF6600;font-size:20px;font-weight:bold;margin-bottom:10px;}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown("<div class='header-bar'>UNITED HATZALAH REAL-TIME DASHBOARD</div>", unsafe_allow_html=True)
st.markdown("<div class='header-spacer'></div>", unsafe_allow_html=True)
st.image("https://israelrescue.org/app/uploads/2023/08/UH-logo.svg", width=200)

# -----------------------
# STATIC MAP
# -----------------------
col1, col2 = st.columns([2, 1])

with col1:
    map_placeholder = st.empty()
with col2:
    pie_placeholder = st.empty()

counter_placeholder = st.empty()
bar_placeholder = st.empty()
story_placeholder = st.empty()

# -----------------------
# AUTO-UPDATE LOOP
# -----------------------
refresh_interval = 10  # seconds
stop_refresh = st.checkbox("Pause Auto-Refresh", value=False)

# Build the map once outside the loop
def build_map(data):
    m = folium.Map(location=[31.8, 35]()
