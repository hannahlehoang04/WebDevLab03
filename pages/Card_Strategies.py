import streamlit as st
import requests
import google.generativeai as genai

# Page config
st.set_page_config(page_title="AI Card Strategies", page_icon="🎯", layout="wide")

# Title and description
st.title("🎯 AI Card Strategies")
st.markdown("""
Get expert card game strategies and analysis powered by AI!
Optionally draw cards from a deck to get specific advice.
""")

# Sidebar for API key and settings
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Gemini API key input
    api_key = st.text_input(
        "🔑 Enter your Gemini API Key",
        type="password",
        help="Get your free API key from https://aistudio.google.com/apikey"
    )
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("✅ API Key configured!")
        except Exception as e:
            st.error(f"❌ Invalid API key: {e}")
    else:
        st.info("👆 Enter your Gemini API key to start")
    
    st.divider()
    
    # Output length customization
    st.subheader("📝 Output Settings")
    output_length = st.slider(
        "Response Length",
        min_value=50,
        max_value=500,
        value=200,
        step=50,
        help="Adjust the maximum word count for AI responses"
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

with col1:
    st.markdown("Draw cards to get context-specific strategies!")

with col2:
    if st.button("🎲 Draw Random Card", use_container_width=True):
        try:
            # Create a new deck if needed
            if 'deck_id' not in st.session_state:
                deck_response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
                st.session_state.deck_id = deck_response.json()['deck_id']
            
            # Draw a card
            draw_response = requests.get(f"https://deckofcardsapi.com/api/deck/{st.session_state.deck_id}/draw/?count=1")
            draw_data = draw_response.json()
            
            if draw_data['success']:
                card = draw_data['cards'][0]
                st.session_state.drawn_card = card
                st.success(f"Drew: {card['value']} of {card['suit']}")
            else:
                st.warning("Deck is empty! Creating a new deck...")
                deck_response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
                st.session_state.deck_id = deck_response.json()['deck_id']
        except Exception as e:
            st.error(f"Error drawing card: {e}")

# Display drawn card if available
if 'drawn_card' in st.session_state:
    card = st.session_state.drawn_card
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(card['image'], width=200)
        st.caption(f"{card['value']} of {card['suit']}")

st.divider()

# Strategy selection
st.subheader("🎯 Select Strategy Type")

strategy_options = {
    "♠️ Poker Strategy": "Provide expert poker strategy and tips",
    "🃏 Blackjack Tips": "Give blackjack strategy and optimal play advice",
    "🎰 Card Probability": "Explain probability and odds for card games",
    "📊 Card Counting Basics": "Teach the fundamentals of card counting",
    "🎲 Game Rules Explanation": "Explain rules for various card games",
    "💡 Beginner Tips": "Provide tips for beginners learning card games",
    "🏆 Advanced Tactics": "Share advanced strategies for experienced players",
    "🎴 Custom Analysis": "Analyze a specific scenario or question"
}

col1, col2 = st.columns(2)

with col1:
    strategy_type = st.selectbox(
        "Choose Strategy Type",
        options=list(strategy_options.keys())
    )

with col2:
    st.info(strategy_options[strategy_type])

# Custom question for custom analysis
if "Custom" in strategy_type:
    custom_question = st.text_area(
        "✍️ Enter your specific question or scenario:",
        placeholder="e.g., What's the best way to play a pair of 8s in blackjack?",
        height=100
    )
else:
    custom_question = None

st.divider()

# Generate strategy button
if st.button("🚀 Generate Strategy", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ Please enter your Gemini API key in the sidebar first!")
    else:
        try:
            # Build the prompt
            prompt_parts = []
            
            # Add detail level instruction
            if detail_level == "Brief":
                prompt_parts.append(f"Provide a brief, concise response (around {output_length} words).")
            elif detail_level == "Moderate":
                prompt_parts.append(f"Provide a moderately detailed response (around {output_length} words).")
            else:
                prompt_parts.append(f"Provide a comprehensive, detailed response (around {output_length} words).")
            
            # Add strategy type
            if "Poker" in strategy_type:
                prompt_parts.append("Provide expert poker strategy, including hand rankings, betting strategies, and position play.")
            elif "Blackjack" in strategy_type:
                prompt_parts.append("Provide blackjack strategy including basic strategy charts, when to hit/stand/double/split.")
            elif "Probability" in strategy_type:
                prompt_parts.append("Explain card game probability, odds calculation, and statistical concepts for card games.")
            elif "Counting" in strategy_type:
                prompt_parts.append("Explain card counting fundamentals, hi-lo system, and how to track cards (for educational purposes only).")
            elif "Rules" in strategy_type:
                prompt_parts.append("Explain rules for popular card games in a clear, easy-to-understand format.")
            elif "Beginner" in strategy_type:
                prompt_parts.append("Provide beginner-friendly tips for learning and improving at card games.")
            elif "Advanced" in strategy_type:
                prompt_parts.append("Share advanced tactics and strategies for experienced card game players.")
            elif "Custom" in strategy_type and custom_question:
                prompt_parts.append(f"Answer this specific card game question: {custom_question}")
            
            # Add card context if available
            if 'drawn_card' in st.session_state:
                card = st.session_state.drawn_card
                prompt_parts.append(f"\nContext: The user has drawn the {card['value']} of {card['suit']}. Include advice specific to this card if relevant.")
            
            full_prompt = " ".join(prompt_parts)
            
            # Generate response with Gemini
            with st.spinner("🤔 AI is analyzing strategies..."):
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(full_prompt)
                
                # Display response
                st.success("✅ Strategy Generated!")
                st.markdown("### 📋 AI Strategy Response:")
                st.markdown(response.text)
                
                # Display word count
                word_count = len(response.text.split())
                st.caption(f"📊 Response length: {word_count} words")
                
        except Exception as e:
            st.error(f"❌ Error generating strategy: {e}")
            st.info("💡 Tip: Make sure your API key is valid and you have an active internet connection.")

# Footer
st.divider()
st.caption("🎴 Card strategies powered by Google Gemini AI | Data from Deck of Cards API")
