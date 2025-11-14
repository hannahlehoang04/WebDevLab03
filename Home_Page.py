import streamlit as st

# Configure page
st.set_page_config(
    page_title="Deck of Cards Lab 03",
    page_icon="🎴",
    layout="wide"
)

# Title
st.title("🎴 Deck of Cards - Web Development Lab03")

# Assignment Data
st.header("CS 1301")
st.subheader("Team 01, Web Development - Section A")
st.subheader("Hannah Hoang, Partner Name")  # Replace with your partner's name

# Introduction
st.write("""
Welcome to our Deck of Cards Streamlit app! Explore the world of playing cards with interactive 
features, AI-powered game strategies, and a chatbot assistant.

🎲 **Navigate through these pages:**

1. **🎴 Card Explorer**: Shuffle decks, draw cards, and visualize card distributions with interactive charts.
2. **🤖 AI Card Strategies**: Use Google Gemini AI to generate game strategies, card combinations, and winning tips.
3. **💬 Card Game Chatbot**: Chat with an AI assistant about card games, rules, and strategies.
4. **📖 Help & About**: Documentation and API information.

""")

st.divider()

# Quick Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Pages", "4")
with col2:
    st.metric("Cards in Deck", "52")
with col3:
    st.metric("API", "Deck of Cards")
with col4:
    st.metric("AI Model", "Gemini Pro")

# Add card image
st.image("https://deckofcardsapi.com/static/img/back.png", 
         caption="Deck of Cards API", width=200)

st.info("👈 Use the sidebar to navigate between pages!")

st.markdown("""
### 🎲 About This Project
This app uses the **Deck of Cards API** to provide an interactive experience with playing cards.
You can shuffle decks, draw cards, analyze card distributions, and get AI-powered insights about 
various card games like Poker, Blackjack, and more!

**API Features:**
- No API key required! ✨
- Real card images (PNG & SVG)
- Full 52-card deck support
- Shuffle, draw, and pile management
- Perfect for game development
""")
