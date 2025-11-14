import streamlit as st

# Configure page
st.set_page_config(
    page_title="Sakura Card Captor Lab 03",
    page_icon="🌸",
    layout="wide"
)

# Title with anime theme
st.title("🌸 Sakura Card Captor - Web Development Lab03")

# Assignment Data
st.header("CS 1301")
st.subheader("Team 01, Web Development - Section A")
st.subheader("Hannah Hoang, Partner Name")  # Replace with your partner's name

# Introduction
st.write("""
Welcome to our Sakura Card Captor Streamlit app! Navigate through the magical pages using the sidebar. 
Explore the mystical Clow Cards and Sakura Cards with AI-powered insights!

✨ **The following magical pages await you:**

1. **🎴 Card Explorer**: Browse and visualize all Clow and Sakura Cards with interactive filters and beautiful card displays.
2. **🤖 AI Card Insights**: Use Google Gemini AI to generate card descriptions, analyze card powers, and create magical stories.
3. **💬 Card Master Chatbot**: Chat with an AI assistant that knows everything about Sakura Card Captor cards.
4. **📖 Help & About**: Documentation on how to use the app and project details.

""")

st.divider()

# Quick Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Pages", "4")
with col2:
    st.metric("Total Cards", "60")
with col3:
    st.metric("API", "Sakura Card Captor")
with col4:
    st.metric("AI Model", "Gemini Pro")

# Add anime-themed description
st.image("https://raw.githubusercontent.com/JessVel/sakura-card-captor-api/main/assets/sakura.jpg", 
         caption="Cardcaptor Sakura - Catch them all!", use_container_width=True)

st.info("👈 Use the sidebar to navigate between magical pages!")

st.markdown("""
### 🌟 About Cardcaptor Sakura
Cardcaptor Sakura is a beloved Japanese manga and anime series. The story follows Sakura Kinomoto, 
a young girl who discovers magical Clow Cards and must capture them all to prevent disaster. 
This app lets you explore all the magical cards from the series!

**API Information:**
- No API key required! ✨
- 60 magical cards with rich data
- Images for both Clow and Sakura card versions
- Data in English, Spanish, and Japanese
""")
