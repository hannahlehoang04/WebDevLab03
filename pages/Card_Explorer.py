import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(page_title="Card Explorer", page_icon="🎴", layout="wide")

st.title("🎴 Card Explorer")
st.write("Shuffle decks, draw cards, and analyze card distributions!")

# Initialize session state
if 'deck_id' not in st.session_state:
    st.session_state.deck_id = None
if 'drawn_cards' not in st.session_state:
    st.session_state.drawn_cards = []

# Sidebar
with st.sidebar:
    st.header("🎲 Deck Controls")
    num_decks = st.slider("Number of Decks", 1, 6, 1)
    
    if st.button("🔀 Create & Shuffle New Deck"):
        try:
            response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={num_decks}")
            data = response.json()
            if data['success']:
                st.session_state.deck_id = data['deck_id']
                st.session_state.drawn_cards = []
                st.success(f"✅ Deck created! ID: {data['deck_id'][:8]}...")
                st.info(f"Cards remaining: {data['remaining']}")
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.divider()
    
    if st.session_state.deck_id:
        st.write(f"**Current Deck:** {st.session_state.deck_id[:8]}...")

# Main content
col1, col2 = st.columns(2)
with col1:
    num_cards = st.number_input("Cards to draw", 1, 52, 5)
with col2:
    view_mode = st.selectbox("View Mode", ["Grid", "List", "Stats"])

if st.button("🎴 Draw Cards", type="primary"):
    if not st.session_state.deck_id:
        st.warning("⚠️ Create a deck first!")
    else:
        try:
            url = f"https://deckofcardsapi.com/api/deck/{st.session_state.deck_id}/draw/?count={num_cards}"
            response = requests.get(url)
            data = response.json()
            
            if data['success']:
                cards = data['cards']
                st.session_state.drawn_cards.extend(cards)
                st.success(f"✅ Drew {len(cards)} cards! Remaining: {data['remaining']}")
                
                if view_mode == "Grid":
                    st.subheader("🎴 Drawn Cards")
                    cols = st.columns(5)
                    for i, card in enumerate(cards):
                        with cols[i % 5]:
                            st.image(card['image'], use_container_width=True)
                            st.caption(f"{card['value']} of {card['suit']}")
                
                elif view_mode == "List":
                    st.subheader("📋 Card List")
                    df = pd.DataFrame([{
                        'Card': f"{c['value']} of {c['suit']}",
                        'Value': c['value'],
                        'Suit': c['suit']
                    } for c in cards])
                    st.dataframe(df, use_container_width=True)
                
                else:
                    st.subheader("📊 Statistics")
                    suits = [c['suit'] for c in cards]
                    suit_counts = Counter(suits)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig = px.pie(values=list(suit_counts.values()),
                                   names=list(suit_counts.keys()),
                                   title="Suit Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        values = [c['value'] for c in cards]
                        value_counts = Counter(values)
                        fig = px.bar(x=list(value_counts.keys()),
                                   y=list(value_counts.values()),
                                   title="Value Distribution")
                        st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

# History
if st.session_state.drawn_cards:
    st.divider()
    st.subheader(f"🎯 Total Drawn: {len(st.session_state.drawn_cards)}")
    with st.expander("View All Cards"):
        df = pd.DataFrame([{
            'Card': f"{c['value']} of {c['suit']}",
            'Suit': c['suit'],
            'Value': c['value']
        } for c in st.session_state.drawn_cards])
        st.dataframe(df)
        csv = df.to_csv(index=False)
        st.download_button("💾 Download CSV", csv, "cards.csv", "text/csv")
