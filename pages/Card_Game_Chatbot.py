import streamlit as st
import requests
import google.generativeai as genai

# Set the page info
st.set_page_config(page_title="Card Game Chatbot", page_icon="🤖", layout="wide")

# Make sure important variables exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "deck_id" not in st.session_state:
    st.session_state.deck_id = None

if "current_cards" not in st.session_state:
    st.session_state.current_cards = []

# Main title
st.title("🤖 Card Game Expert Chatbot")
st.write("Ask me anything about card games! I can also see the cards you draw.")

# -----------------------------
# SIDEBAR SECTION
# -----------------------------
with st.sidebar:
    st.header("Settings")

    # Get Gemini API key from user
    api_key = st.text_input("Gemini API Key", type="password")

    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API Key set!")
        except:
            st.error("API Key is invalid.")

    st.write("---")

    # Draw cards
    st.subheader("Draw Cards")

    num_cards = st.number_input(
        "Number of cards:",
        min_value=1,
        max_value=10,
        value=1
    )

    if st.button("Draw Cards"):
        try:
            # If no deck exists, make a new one
            if st.session_state.deck_id is None:
                new_deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
                st.session_state.deck_id = new_deck.json()["deck_id"]

            # Draw cards from the API
            draw = requests.get(
                f"https://deckofcardsapi.com/api/deck/{st.session_state.deck_id}/draw/?count={num_cards}"
            ).json()

            # If deck is empty, reset it
            if not draw["success"]:
                new_deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
                st.session_state.deck_id = new_deck.json()["deck_id"]
            else:
                st.session_state.current_cards = draw["cards"]
                st.success("Cards Drawn!")
        except:
            st.error("Something went wrong while drawing cards.")

    # Clear cards
    if st.button("Clear Cards"):
        st.session_state.current_cards = []
        st.success("Cards cleared!")

    # Display the cards
    if st.session_state.current_cards:
        st.subheader("Your Cards")
        for c in st.session_state.current_cards:
            st.image(c["image"], width=80)
            st.write(c["value"], " of ", c["suit"])

    st.write("---")

    # Clear chat
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat cleared!")

# ---------------------------------
# MAIN CHAT AREA
# ---------------------------------

st.header("Chat")

# Show old messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input box
user_msg = st.text_area("Type something:")

# Send button
if st.button("Send Message"):
    if not api_key:
        st.error("Enter your API key first.")
    elif user_msg.strip() == "":
        st.warning("Please type something.")
    else:
        # Add user's message to the chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_msg
        })

        # Build prompt
        prompt = "You are a friendly card game assistant.\n"

        # Add card info
        if st.session_state.current_cards:
            card_text = ", ".join(
                c["value"] + " of " + c["suit"]
                for c in st.session_state.current_cards
            )
            prompt += "User currently has these cards: " + card_text + "\n"

        # Add recent chat history (just the last few messages)
        prompt += "\nConversation so far:\n"
        for m in st.session_state.chat_history[-6:-1]:
            if m["role"] == "user":
                prompt += "User: " + m["content"] + "\n"
            else:
                prompt += "Assistant: " + m["content"] + "\n"

        # Add the new message
        prompt += "User's question: " + user_msg

        # Ask Gemini
        try:
            model = genai.GenerativeModel("gemini-pro")
            reply = model.generate_content(prompt).text

            # Add assistant response
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": reply
            })

            st.rerun()  # refresh screen so message appears cleanly
        except:
            st.error("Something went wrong with Gemini.")

# ------------------------------
# QUICK QUESTION BUTTONS
# ------------------------------
st.write("---")
st.header("Quick Questions")

quick_list = [
    "Explain poker hand rankings",
    "Best blackjack strategy?",
    "How do I count cards?",
    "Card probability basics",
    "Tips for beginners",
    "Rules for popular games"
]

cols = st.columns(3)

for i in range(len(quick_list)):
    if cols[i % 3].button(quick_list[i]):
        # Add question to chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": quick_list[i]
        })

        # Basic prompt for quick answer
        q_prompt = "You are a card game expert. Answer this: " + quick_list[i]

        if st.session_state.current_cards:
            card_text = ", ".join(
                c["value"] + " of " + c["suit"]
                for c in st.session_state.current_cards
            )
            q_prompt += "\nUser's cards: " + card_text

        # Ask Gemini
        try:
            model = genai.GenerativeModel("gemini-pro")
            ans = model.generate_content(q_prompt).text

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": ans
            })
            st.rerun()
        except:
            st.error("Error answering quick question.")
