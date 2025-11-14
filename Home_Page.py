import streamlit as st
import requests

# Configure page
st.set_page_config(
    page_title="Chess.com API Lab 03",
    page_icon="♟️",
    layout="wide"
)

# Title
st.title("♟️ Chess.com API - Web Development Lab03")

# Assignment Data
st.header("CS 1301")
st.subheader("Team 75, Web Development Lab03 - Section A")
st.subheader("Hannah LeHoang, Mason Bird")

# Introduction
st.write("""
Welcome to our Chess.com API Streamlit app! Explore the world of chess with player statistics,
game analysis, and interactive features powered by the Chess.com Published Data API.

♟️ **Navigate through these pages:**

1. 👤 Player Profile: Search for any Chess.com player and view their profile, ratings, and statistics.
2. 🎮 Game History: Explore a player's game archives and analyze their matches.
3. 🏆 Leaderboards: View top players and rankings across different game modes.
4. 📊 Statistics Dashboard: Visualize player performance with interactive charts and graphs.
5. 📖 Help & About: API documentation and project information.
""")

st.divider()

# Quick Stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Pages", "5")
    
with col2:
    st.metric("API", "Chess.com")
    
with col3:
    st.metric("Data Format", "JSON")
    
with col4:
    st.metric("Rate Limit", "300/min")

# Add chess image
st.image("https://images.chesscomfiles.com/uploads/v1/images_users/tiny_mce/SamCopeland/phpmeXx6V.png", 
         caption="Chess.com - Play Chess Online", width=400)

st.info("👈 Use the sidebar to navigate between pages!")

st.markdown("""
### ♟️ About This Project

This app uses the **Chess.com Published Data API** to provide comprehensive chess player analysis.
You can search for players, view their statistics, analyze game history, and explore leaderboards!

**API Features:**
- Player profiles and ratings
- Game archives (PGN format)
- Live and daily chess statistics  
- Club and tournament data
- Titled player listings
- Streamers and content creators

**Tech Stack:**
- Streamlit for web interface
- Requests for API calls
- Pandas for data manipulation
- Plotly for interactive visualizations
""")

# Test API Connection
st.divider()
st.subheader("🔌 API Connection Test")

try:
    response = requests.get("https://api.chess.com/pub/player/magnuscarlsen")
    if response.status_code == 200:
        st.success("✅ Successfully connected to Chess.com API!")
        data = response.json()
        st.write(f"Sample data fetched for player: **{data.get('username', 'N/A')}**")
    else:
        st.error(f"❌ API connection failed with status code: {response.status_code}")
except Exception as e:
    st.error(f"❌ Error connecting to API: {str(e)}")
