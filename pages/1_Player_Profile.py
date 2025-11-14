import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Player Profile", page_icon="👤", layout="wide")

st.title("👤 Chess.com Player Profile")

st.markdown("""
Search for any Chess.com player to view their profile, ratings, and statistics.
The Chess.com API provides comprehensive player data including:
- Player profile information
- Current ratings across different game modes  
- Player statistics and performance metrics
- Account status and titles
""")

st.divider()

# Search input
col1, col2 = st.columns([3, 1])
with col1:
    username = st.text_input(
        "Enter Chess.com Username", 
        value="magnuscarlsen",
        help="Enter the username (case-insensitive)"
    )
with col2:
    search_button = st.button("🔍 Search Player", type="primary", use_container_width=True)

if search_button or username:
    if username:
        with st.spinner(f"Fetching data for {username}..."):
            try:
                # Fetch player profile
                profile_url = f"https://api.chess.com/pub/player/{username.lower()}"
                response = requests.get(profile_url)
                
                if response.status_code == 200:
                    player_data = response.json()
                    
                    # Display player profile
                    st.success(f"✅ Player found: {player_data.get('username', 'N/A')}")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        # Player image
                        if 'avatar' in player_data:
                            st.image(player_data['avatar'], width=200)
                        else:
                            st.info("No avatar available")
                    
                    with col2:
                        st.subheader("Profile Information")
                        
                        # Display profile data
                        st.write(f"**Username:** {player_data.get('username', 'N/A')}")
                        st.write(f"**Player ID:** {player_data.get('player_id', 'N/A')}")
                        st.write(f"**URL:** [View on Chess.com]({player_data.get('url', '#')})")
                        
                        if 'name' in player_data:
                            st.write(f"**Name:** {player_data['name']}")
                        
                        if 'title' in player_data:
                            st.write(f"**Title:** 🏆 {player_data['title']}")
                        
                        if 'status' in player_data:
                            st.write(f"**Status:** {player_data['status']}")
                        
                        if 'country' in player_data:
                            st.write(f"**Country:** [View]({player_data['country']})")
                        
                        if 'joined' in player_data:
                            joined_date = datetime.fromtimestamp(player_data['joined'])
                            st.write(f"**Joined:** {joined_date.strftime('%B %d, %Y')}")
                        
                        if 'last_online' in player_data:
                            last_online = datetime.fromtimestamp(player_data['last_online'])
                            st.write(f"**Last Online:** {last_online.strftime('%B %d, %Y %H:%M')}")
                        
                        if 'followers' in player_data:
                            st.write(f"**Followers:** {player_data['followers']:,}")
                    
                    st.divider()
                    
                    # Fetch player stats
                    stats_url = f"https://api.chess.com/pub/player/{username.lower()}/stats"
                    stats_response = requests.get(stats_url)
                    
                    if stats_response.status_code == 200:
                        stats_data = stats_response.json()
                        
                        st.subheader("📊 Player Statistics & Ratings")
                        
                        # Create tabs for different game modes
                        tabs = []
                        tab_data = []
                        
                        if 'chess_rapid' in stats_data:
                            tabs.append("⚡ Rapid")
                            tab_data.append(('rapid', stats_data['chess_rapid']))
                        
                        if 'chess_blitz' in stats_data:
                            tabs.append("🎯 Blitz")
                            tab_data.append(('blitz', stats_data['chess_blitz']))
                        
                        if 'chess_bullet' in stats_data:
                            tabs.append("💥 Bullet")
                            tab_data.append(('bullet', stats_data['chess_bullet']))
                        
                        if 'chess_daily' in stats_data:
                            tabs.append("📅 Daily")
                            tab_data.append(('daily', stats_data['chess_daily']))
                        
                        if tabs:
                            tab_objects = st.tabs(tabs)
                            
                            for tab, (mode_name, mode_data) in zip(tab_objects, tab_data):
                                with tab:
                                    col1, col2, col3, col4 = st.columns(4)
                                    
                                    with col1:
                                        if 'last' in mode_data:
                                            st.metric("Current Rating", mode_data['last'].get('rating', 'N/A'))
                                    
                                    with col2:
                                        if 'best' in mode_data:
                                            st.metric("Best Rating", mode_data['best'].get('rating', 'N/A'))
                                    
                                    with col3:
                                        if 'record' in mode_data:
                                            record = mode_data['record']
                                            wins = record.get('win', 0)
                                            losses = record.get('loss', 0)
                                            draws = record.get('draw', 0)
                                            total = wins + losses + draws
                                            st.metric("Total Games", total)
                                    
                                    with col4:
                                        if 'record' in mode_data:
                                            record = mode_data['record']
                                            wins = record.get('win', 0)
                                            losses = record.get('loss', 0)
                                            total_decisive = wins + losses
                                            if total_decisive > 0:
                                                win_rate = (wins / total_decisive) * 100
                                                st.metric("Win Rate", f"{win_rate:.1f}%")
                                    
                                    # Display detailed record
                                    if 'record' in mode_data:
                                        st.write("#### Game Record")
                                        record = mode_data['record']
                                        st.write(f"🏆 **Wins:** {record.get('win', 0)}")
                                        st.write(f"❌ **Losses:** {record.get('loss', 0)}")
                                        st.write(f"🤝 **Draws:** {record.get('draw', 0)}")
                        else:
                            st.info("No game statistics available for this player.")
                    
                    # Display raw JSON data (collapsible)
                    with st.expander("📝 View Raw JSON Data"):
                        st.json(player_data)
                        if stats_response.status_code == 200:
                            st.json(stats_data)
                
                elif response.status_code == 404:
                    st.error(f"❌ Player '{username}' not found. Please check the username and try again.")
                else:
                    st.error(f"❌ Error: Received status code {response.status_code}")
            
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please enter a username to search.")

st.divider()

st.markdown("""
### 💡 Popular Chess.com Players to Try:

- **magnuscarlsen** - World Champion
- **hikaru** - GM Hikaru Nakamura  
- **gothamchess** - Popular chess streamer
- **botezlive** - Alexandra Botez
- **chesscom** - Chess.com official account
""")
