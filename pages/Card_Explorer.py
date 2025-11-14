import streamlit as st
import requests
import pandas as pd
from collections import Counter

st.title("Card Explorer")

# Set up session values
if "deck_id" not in st.session_state:
    st.session_state.deck_id = ""
if "drawn" not in st.session_state:
    st.session_state.drawn = []

st.write("Use this app to create a deck, draw cards, and see some simple stats.")

#CREATE DECK 
st.header("Create / Shuffle Deck")

num_decks = st.slider("How many decks?", 1, 6, 1)

if st.button("Create New Deck"):
    url = f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={num_decks}"
    r = requests.get(url).json()
    if r["success"]:
        st.session_state.deck_id = r["deck_id"]
        st.session_state.drawn = []
        st.success("Deck created!")
    else:
        st.error("Could not create deck.")

if st.session_state.deck_id != "":
    st.write("Current Deck ID:", st.session_state.deck_id)

st.write("---")

#DRAW CARDS
st.header("Draw Cards")

count = st.number_input("How many cards to draw?", 1, 52, 5)

view_type = st.selectbox("How do you want to view them?",
                         ["Grid", "List", "Stats"])

if st.button("Draw"):
    if st.session_state.deck_id == "":
        st.warning("Create a deck first.")
    else:
        url = f"https://deckofcardsapi.com/api/deck/{st.session_state.deck_id}/draw/?count={count}"
        r = requests.get(url).json()

        if r["success"]:
            cards = r["cards"]
            st.session_state.drawn.extend(cards)
            st.success("Cards drawn!")

            #GRID VIEW
            if view_type == "Grid":
                st.subheader("Cards")
                cols = st.columns(5)
                for i, c in enumerate(cards):
                    with cols[i % 5]:
                        st.image(c["image"])
                        st.write(c["value"], "of", c["suit"])

            #LIST VIEW
            elif view_type == "List":
                st.subheader("Card List")
                data = []
                for c in cards:
                    data.append({
                        "Card": c["value"] + " of " + c["suit"],
                        "Value": c["value"],
                        "Suit": c["suit"]
                    })
                st.dataframe(pd.DataFrame(data))

            #SIMPLE STATS VIEW
            else:
                st.subheader("Stats")

                suits = [c["suit"] for c in cards]
                values = [c["value"] for c in cards]

                st.write("Suit Counts:", dict(Counter(suits)))
                st.write("Value Counts:", dict(Counter(values)))

        else:
            st.error("Could not draw cards.")

st.write("---")

#HISTORY
if len(st.session_state.drawn) > 0:
    st.header("All Cards Drawn So Far")

    all_data = []
    for c in st.session_state.drawn:
        all_data.append({
            "Card": c["value"] + " of " + c["suit"],
            "Suit": c["suit"],
            "Value": c["value"]
        })

    df = pd.DataFrame(all_data)
    st.dataframe(df)

    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, "cards.csv")
