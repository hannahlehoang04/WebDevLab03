import streamlit as st

# Configure page
st.set_page_config(
    page_title="Chess Lab 03",
    page_icon="♟",
    layout="wide"
)

# Title
st.title("♟ Chess - Web Development Lab03")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 01, Web Development")
st.subheader("Hannah Lehoang, Mason Bird")  # Replace with your partner's name

# Introduction
st.write("""
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. Card Explorer: Shuffle decks, draw cards, and visualize card distributions with interactive charts.
2. Card Strategies: Use Google Gemini AI to generate game strategies, card combinations, and winning tips.
3. Card Game Chatbot: Chat with an AI assistant about card games, rules, and strategies.
4. Help & About: Documentation and API information.

""")

# Add a chess-themed image
st.image("https://images.unsplash.com/photo-1586165368502-1bad197a6461?w=800", 
         caption="Strategic Thinking with Chess", 
         width=700)
