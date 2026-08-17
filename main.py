import streamlit as st
import pyshorteners
import pandas as pd
import random
import string
from datetime import datetime

# Page configuration for a premium look
st.set_page_config(
    page_title="SnapURL - Premium Link Shortener SaaS",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS for styling
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(45deg, #ff4b4b, #ff7676);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4); }
    .metric-card {
        background-color: #1e222b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Analytics Data Simulation
if 'history' not in st.session_state:
    st.session_state.history = []

def generate_mock_analytics():
    countries = ['United States', 'United Kingdom', 'Pakistan', 'Germany', 'United Arab Emirates', 'Canada']
    browsers = ['Chrome', 'Safari', 'Firefox', 'Edge']
    return {
        'country': random.choice(countries),
        'browser': random.choice(browsers),
        'clicks': random.randint(15, 250)
    }

# App Header
st.title("🔗 SnapURL — Advanced Link Shortener SaaS")
st.caption("A production-ready micro-SaaS platform asset for digital entrepreneurs.")

# Sidebar Information for Flippa Buyers
with st.sidebar:
    st.header("⚡ SaaS Asset Info")
    st.markdown("""
    * **Product:** URL Shortener & Analytics Tool
    * **Framework:** Streamlit (Pure Python)
    * **Database Ready:** Session-based (Can scale to SQL)
    * **Monetization Option:** Add AdMob, Premium Plans, or API Access.
    """)
    st.info("💡 **Tip for Buyer:** You can easily connect this frontend to MongoDB or PostgreSQL for persistent user database management.")

# Main Dashboard Layout
tab1, tab2, tab3 = st.tabs(["🚀 Shorten Link", "📊 Live Analytics Dashboard", "📋 Managed Links History"])

with tab1:
    st.subheader("Create a Short URL")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        long_url = st.text_input("Enter your long URL here:", placeholder="https://example.com")
    with col2:
        custom_alias = st.text_input("Custom Alias (Optional):", placeholder="promo2026", max_chars=15)
        
    if st.button("Shorten URL"):
        if long_url:
            try:
                # Shortening logic
                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(long_url)
                
                # Apply custom alias if provided (Visual simulation for SaaS presentation)
                if custom_alias:
                    short_url = f"https://tinyurl.com{custom_alias}"
                
                st.success("🎉 URL Shortened Successfully!")
                st.code(short_url, language="text")
                
                # Mock analytical metrics generation for asset showcase value
                analytics = generate_mock_analytics()
                
                # Save data to session history
                st.session_state.history.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "original": long_url,
                    "short": short_url,
                    "alias": custom_alias if custom_alias else "None",
                    "clicks": analytics['clicks'],
                    "top_country": analytics['country'],
                    "top_browser": analytics['browser']
                })
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid URL first.")

with tab2:
    st.subheader("📈 Real-time Traffic Analytics")
    if len(st.session_state.history) > 0:
        # Create Dataframe from history
        df = pd.DataFrame(st.session_state.history)
        
        # Display Key Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='metric-card'><h4>Total Links Tracked</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-card'><h4>Total Simulated Clicks</h4><h2>{df['clicks'].sum()}</h2></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-card'><h4>Top Performing Country</h4><h2>{df['top_country'].mode()[0]}</h2></div>", unsafe_allow_html=True)
            
        st.write("")
        st.subheader("Clicks Distribution per Link")
        st.bar_chart(data=df, x="short", y="clicks")
        
    else:
        st.info("No analytics data available yet. Shorten a link in the first tab to populate the charts.")

with tab3:
    st.subheader("🗂️ All Active Links")
    if len(st.session_state.history) > 0:
        df_history = pd.DataFrame(st.session_state.history)
        st.dataframe(df_history[["time", "original", "short", "alias", "clicks"]], use_container_width=True)
    else:
        st.info("Your link database history is currently empty.")
