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
    max-height: 400px;
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
    font-size: 15px;
    line-height: 1.6;
    text-align: justify;
}

/* Tooltip styling (hover snippet) */
.leaflet-tooltip {
    font-size: 12px !important;
    max-width: 180px !important;
    white-space: normal !important;
    word-wrap: break-word !important;
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
    <div class='counter-title'>
