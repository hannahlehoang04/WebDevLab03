import streamlit as st
import requests
import google.generativeai as genai
import time

# Page config
st.set_page_config(page_title="Card Game Chatbot", page_icon="🤖", layout="wide")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'deck_id' not in st.session_state:
    st.session_state.deck_id = None

if 'current_cards' not in st.session_state:
    st.session_state.current_cards = []

# Title
st.title("🤖 Card Game Expert Chatbot")
st.markdown("""
Ask me anything about card games! I'm powered by AI and have access to live card data.
I remember our conversation and can provide personalized advice.
""")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "🔑 Gemini API Key",
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
        st.info("👆 Enter your Gemini API key to start chatting")
    
    st.divider()
    
    # Card context controls
    st.subheader("🎴 Live Card Context")
    st.markdown("Draw cards to give the chatbot context about your current hand!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_cards = st.number_input(
            "Cards to draw",
            min_value=1,
            max_value=10,
            value=1
        )
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        if st.button("🎲 Draw Cards", use_container_width=True):
            try:
                # Create or shuffle deck
                if not st.session_state.deck_id:
                    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
                    st.session_state.deck_id = response.json()['deck_id']
                
                # Draw cards
                draw_response = requests.get(
                    f"https://deckofcardsapi.com/api/deck/{st.session_state.deck_id}/draw/?count={num_cards}"
                )
                draw_data = draw_response.json()
                
                if draw_data['success'] and draw_data['cards']:
                    st.session_state.current_cards = draw_data['cards']
                    st.success(f"✅ Drew {len(draw_data['cards'])} card(s)!")
                else:
                    # Deck empty, create new one
                    response = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
                    st.session_state.deck_id = response.json()['deck_id']
                    st.warning("♻️ Deck was empty, created a new one!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    if st.button("🗑️ Clear Cards", use_container_width=True):
        st.session_state.current_cards = []
        st.success("✅ Cards cleared!")
    
    # Display current cards
    if st.session_state.current_cards:
        st.markdown("**Current Cards:**")
        for card in st.session_state.current_cards:
            st.image(card['image'], width=80)
            st.caption(f"{card['value']} of {card['suit']}")
    
    st.divider()
    
    # Clear chat button
    if st.button("🚮 Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.success("✅ Chat history cleared!")
    
    # Display message count
    st.caption(f"💬 Messages: {len(st.session_state.chat_history)}")

st.divider()

# Display chat history
st.subheader("💬 Conversation")

if st.session_state.chat_history:
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            with st.chat_message("user", avatar="👤"):
                st.markdown(message['content'])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message['content'])
else:
    st.info("👋 Start a conversation! Ask me anything about card games.")

st.divider()

# Chat input
st.subheader("✍️ Your Message")

user_input = st.text_area(
    "Type your message here:",
    placeholder="e.g., What's the probability of getting a royal flush in poker?",
    height=100,
    key="user_input_field"
)

if st.button("📤 Send Message", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ Please enter your Gemini API key in the sidebar first!")
    elif not user_input or user_input.strip() == "":
        st.warning("⚠️ Please enter a message!")
    else:
        try:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input
            })
            
            # Build context for AI
            context_parts = []
            
            # Add system prompt
            context_parts.append(
                "You are a helpful card game expert chatbot. You provide accurate, friendly advice about card games, "
                "strategies, rules, and probabilities. Keep responses concise but informative."
            )
            
            # Add card context if available
            if st.session_state.current_cards:
                cards_desc = ", ".join([
                    f"{card['value']} of {card['suit']}" 
                    for card in st.session_state.current_cards
                ])
                context_parts.append(
                    f"\nCurrent cards in the user's hand: {cards_desc}. "
                    "Consider these cards when providing advice if relevant to the question."
                )
            
            # Add conversation history (last 5 messages for context)
            recent_history = st.session_state.chat_history[-6:-1]  # Exclude the message we just added
            if recent_history:
                context_parts.append("\nRecent conversation:")
                for msg in recent_history:
                    role_label = "User" if msg['role'] == 'user' else "Assistant"
                    context_parts.append(f"{role_label}: {msg['content']}")
            
            # Add current user question
            context_parts.append(f"\nUser's current question: {user_input}")
            
            full_prompt = "\n".join(context_parts)
            
            # Generate response
            with st.spinner("🤔 Thinking..."):
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(full_prompt)
                
                # Add assistant response to history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response.text
                })
                
                # Success message
                st.success("✅ Response generated!")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("💡 Make sure your API key is valid and you have internet connection.")

# Quick question buttons
st.divider()
st.subheader("⚡ Quick Questions")

col1, col2, col3 = st.columns(3)

quick_questions = [
    "🂠 Explain poker hand rankings",
    "🃏 Best blackjack strategy?",
    "🎲 How do I count cards?",
    "📊 Card probability basics",
    "🎯 Tips for beginners",
    "🎴 Rules for popular games"
]

for i, question in enumerate(quick_questions):
    col = [col1, col2, col3][i % 3]
    with col:
        if st.button(question, use_container_width=True, key=f"quick_{i}"):
            # Set the question in the text area by adding it to chat directly
            if api_key:
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': question.split(" ", 1)[1]  # Remove emoji
                })
                
                # Generate response for quick question
                try:
                    context = f"You are a card game expert. Answer this question concisely: {question.split(' ', 1)[1]}"
                    
                    if st.session_state.current_cards:
                        cards_desc = ", ".join([
                            f"{card['value']} of {card['suit']}" 
                            for card in st.session_state.current_cards
                        ])
                        context += f"\nUser's current cards: {cards_desc}"
                    
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(context)
                    
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response.text
                    })
                    
                    st.rerun()
                except:
                    st.error("Error processing quick question")
            else:
                st.warning("Please enter your API key first!")

# Footer
st.divider()
st.caption("🤖 Chatbot powered by Google Gemini AI | Card data from Deck of Cards API")
