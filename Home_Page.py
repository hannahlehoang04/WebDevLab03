import streamlit as st

# Configure page
st.set_page_config(
    page_title="Chess Lab 03",
    page_icon="♟",
    layout="wide"
)

# Title
st.title("♟ Chess - Web Development Lab03")

# Course info
st.header("CS 1301")

# Team info
st.subheader("Team 01, Web Development")

# Student names
st.subheader("Hannah Lehoang, Mason Bird")  # Replace with your partner's name

# Add a chess-themed image
st.image("https://images.unsplash.com/photo-1586165368502-1bad197a6461?w=800", 
         caption="Strategic Thinking with Chess", 
         width=700)
