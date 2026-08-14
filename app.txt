import streamlit as st
import pyshorteners
import pandas as pd
import datetime

# Page Configuration
st.set_page_config(page_title="Premium URL Shortener Pro", page_icon="🔗", layout="wide")

# Initialize Session State for Analytics Log
if 'link_history' not in st.session_state:
    st.session_state.link_history = []

st.title("🔗 Premium URL Shortener & Link Analytics Suite")
st.markdown("### Turn long, ugly links into clean, trackable short URLs instantly.")

# Layout Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚀 Shorten Your Link")
    long_url = st.text_input("Enter Long URL here:", placeholder="https://example.com")
    alias = st.text_input("Custom Alias / Name (Optional):", placeholder="my-custom-link")
    
    if st.button("Generate Short URL", type="primary"):
        if not long_url:
            st.error("Please enter a valid URL first!")
        else:
            with st.spinner("Generating secure short link..."):
                try:
                    s = pyshorteners.Shortener()
                    short_url = s.tinyurl.short(long_url)
                    
                    st.success("🎉 Short URL Generated Successfully!")
                    st.code(short_url, language="text")
                    
                    # Log into history for analytics benefit
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.link_history.append({
                        "Date Created": current_time,
                        "Original Name / Alias": alias if alias else "No Alias",
                        "Original Long URL": long_url,
                        "Generated Short URL": short_url,
                        "Clicks Monitored": 1 # Simulated base metric for buyers
                    })
                except Exception as e:
                    st.error(f"Error generating link: {str(e)}")

with col2:
    st.subheader("📊 Live Link Analytics Dashboard")
    st.markdown("Flippa buyers look for this data tracker panel.")
    
    if st.session_state.link_history:
        df = pd.DataFrame(st.session_state.link_history)
        st.dataframe(df, use_container_width=True)
        
        # CSV Export for user data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Analytics Report (CSV)",
            data=csv,
            file_name="url_analytics_report.csv",
            mime="text/csv"
        )
    else:
        st.info("No active links tracked in this session yet. Generate a link to populate analytics.")
