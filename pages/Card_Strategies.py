import streamlit as st
import requests
import google.generativeai as genai

# -------------------------------------------
# Basic setup for the page
# -------------------------------------------
st.set_page_config(page_title="AI Card Strategies", page_icon="🎯", layout="wide")

st.title("🎯 AI Card Strategies")
st.write("Get simple card game tips and analysis using AI. You can also draw cards for more specific advice!")

# -------------------------------------------
# SIDEBAR
# -------------------------------------------
with st.sidebar:
    st.header("Configuration")

    # Ask for API key
    api_key = st.text_input("Enter Gemini API Key:", type="password")

    # Try enabling Gemini
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API Key set!")
        except:
            st.error("API Key invalid.")
    else:
        st.info("Enter your API key to begin.")

    st.write("---")

    # Choose how detailed the AI should be
    st.subheader("Response Settings")

    output_length = st.slider(
        "Maximum Words",
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

st.write("---")

# -------------------------------------------
# DRAW A CARD
# -------------------------------------------
st.subheader("Draw a Card (Optional)")

left, right = st.columns([2, 1])

with right:
    if st.button("Draw Card"):
        try:
            # Make a deck if we don't have one yet
            if "deck_id" not in st.session_state:
                new_deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()
                st.session_state.deck_id = new_deck["deck_id"]

            # Draw 1 card
            draw = requests.get(
                f"https://deckofcardsapi.com/api/deck/{st.session_state.deck_id}/draw/?count=1"
            ).json()

            if draw["success"]:
                st.session_state.drawn_card = draw["cards"][0]
            else:
                # Reset deck if empty
                new_deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()
                st.session_state.deck_id = new_deck["deck_id"]
        except:
            st.error("Error drawing card.")

# Show card if drawn
if "drawn_card" in st.session_state:
    card = st.session_state.drawn_card
    st.image(card["image"], width=200)
    st.caption(f"{card['value']} of {card['suit']}")

st.write("---")

# -------------------------------------------
# STRATEGY TYPE SELECTION
# -------------------------------------------
st.subheader("Choose Strategy Type")

strategy_list = {
    "Poker Strategy": "Expert poker advice",
    "Blackjack Tips": "Blackjack playing advice",
    "Card Probability": "Explain card odds",
    "Card Counting Basics": "Teach basic counting ideas",
    "Game Rules Explanation": "Explain common game rules",
    "Beginner Tips": "Helpful tips for new players",
    "Advanced Tactics": "Experienced player strategies",
    "Custom Analysis": "Give custom strategy answer"
}

colA, colB = st.columns(2)

with colA:
    strategy_type = st.selectbox("Select Strategy", list(strategy_list.keys()))

with colB:
    st.info(strategy_list[strategy_type])

# Custom question text box
custom_question = ""
if strategy_type == "Custom Analysis":
    custom_question = st.text_area(
        "Enter your custom question:",
        placeholder="Example: How should I play a pair of 8s in blackjack?"
    )

st.write("---")

# -------------------------------------------
# GENERATE STRATEGY BUTTON
# -------------------------------------------
if st.button("Generate Strategy", type="primary"):
    if not api_key:
        st.error("Enter your API Key!")
    else:
        try:

            # -------------------------
            # Build prompt step-by-step
            # -------------------------
            prompt = ""

            # Add detail level
            if detail_level == "Brief":
                prompt += f"Give a short response (~{output_length} words). "
            elif detail_level == "Moderate":
                prompt += f"Give a moderately detailed response (~{output_length} words). "
            else:
                prompt += f"Give a detailed, thorough response (~{output_length} words). "

            # Add topic
            if strategy_type == "Poker Strategy":
                prompt += "Explain poker strategy, hand rankings, and common tips. "
            elif strategy_type == "Blackjack Tips":
                prompt += "Give blackjack tips including when to hit, stand, split, or double. "
            elif strategy_type == "Card Probability":
                prompt += "Explain basic probability in card games. "
            elif strategy_type == "Card Counting Basics":
                prompt += "Explain card counting in a simple educational way. "
            elif strategy_type == "Game Rules Explanation":
                prompt += "Explain card game rules clearly. "
            elif strategy_type == "Beginner Tips":
                prompt += "Give beginner-friendly card game tips. "
            elif strategy_type == "Advanced Tactics":
                prompt += "Explain advanced card-playing tactics. "
            elif strategy_type == "Custom Analysis":
                prompt += f"Answer this question: {custom_question}. "

            # If card is drawn, add context
            if "drawn_card" in st.session_state:
                card = st.session_state.drawn_card
                prompt += f"The user drew the card: {card['value']} of {card['suit']}. "

            # --------------------------------
            # CALL GEMINI AI
            # --------------------------------
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)

            # Show result
            st.subheader("AI Strategy Response")
            st.write(response.text)

            # Word count
            wc = len(response.text.split())
            st.caption(f"Word count: {wc}")

        except Exception as e:
            st.error("Error generating strategy.")
            st.write(e)

st.write("---")
st.caption("AI strategies powered by Gemini | Cards from Deck of Cards API")
