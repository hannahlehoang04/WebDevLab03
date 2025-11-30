import streamlit as st
import requests
import google.generativeai as genai

# Hard-coded API key (CS 1301 simple method)
# Replace this with your real API key!
api_key = "YOUR_API_KEY_HERE"

# Configure Gemini with the hard-coded key
try:
    genai.configure(api_key=api_key)
except:
    print("API key error")

# Page config
st.set_page_config(page_title="AI Card Strategies", page_icon="🎯", layout="wide")

# Title and description
st.title("🎯 AI Card Strategies")
st.markdown("""
Get expert card game strategies and analysis powered by AI!
Optionally draw cards from a deck to get specific advice.
""")

# Sidebar (still shows the field, but key is already set)
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.success("API Key already loaded in code.")

    st.divider()

    # Output length customization
    st.subheader("📝 Output Settings")
    output_length = st.slider(
        "Response Length",
        min_value=50,
        max_value=500,
        value=200,
        step=50
    )
    
    detail_level = st.select_slider(
        "Detail Level",
        options=["Brief", "Moderate", "Detailed"],
        value="Moderate"
    )

st.divider()

# Optional card drawing feature
st.subheader("🎴 Optional: Draw Cards for Specific Analysis")

col1, col2 = st.columns([2, 1])
