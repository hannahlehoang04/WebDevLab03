import streamlit as st

# Configure page
st.set_page_config(
    page_title="Web Dev Lab 03",
    page_icon="🌤️",
    layout="wide"
)

# Title of App
st.title("🌤️ Web Development Lab03")

# Assignment Data
st.header("CS 1301")
st.subheader("Team 75, Web Development - Section A")
st.subheader("Hannah LeHoang, Mason Bird") 

# Introduction
st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. **Weather Data Analysis**: Interactive visualization of current weather data for any city worldwide with temperature trends and atmospheric conditions.
2. **AI Weather Insights**: Uses Google Gemini AI to generate detailed weather summaries, forecasts, and travel recommendations based on current conditions.
3. **Weather Q&A Chatbot**: Conversational AI assistant that answers weather-related questions using real-time API data and maintains conversation history.
4. **Help & About**: Documentation on how to use the app, API information, and project development details.

""")

st.divider()

# Quick Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pages", "4")
with col2:
    st.metric("API Used", "OpenWeatherMap")
with col3:
    st.metric("AI Model", "Gemini Pro")

st.info("👈 Use the sidebar to navigate between pages!")
