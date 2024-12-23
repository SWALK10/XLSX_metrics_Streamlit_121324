import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="ETF Analysis Dashboard", layout="wide")

# Custom CSS for the banner, input area, and table styling
st.markdown("""
    <style>
    .banner {
        text-align: center;
        padding: 0;
        margin: 0;
    }
    .banner h1 {
        color: #1E3D59;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    .banner h2 {
        color: #17263A;
        font-size: 1.8em;
        font-weight: bold;
        margin-top: 0.2em;
    }
    /* New styles for ticker input area */
    .ticker-input-area {
        margin: 1em 0;
        padding: 1em;
        background: #f8f9fa;
        border-radius: 5px;
    }
    .stTextInput > label {
        font-size: 0.9em !important;
        color: #1E3D59 !important;
    }
    .stButton > button {
        float: right;
        margin-top: -3.5em;
    }
    </style>
""", unsafe_allow_html=True)

# Banner with logo
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<div class="banner"><h1>ETF Analysis Dashboard</h1></div>', unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="logo-placeholder">
            LOGO
        </div>
    """, unsafe_allow_html=True)

# Ticker Input Area (New)
st.markdown('<div class="ticker-input-area">', unsafe_allow_html=True)
col1, col2 = st.columns([3,1])
with col1:
    ticker_input = st.text_input(
        "Enter ETF Tickers",
        placeholder="Enter comma-separated tickers (e.g., SPY, QQQ, IWM)",
        label_visibility="visible",
        key="ticker_input"
    )
with col2:
    analyze_button = st.button("Analyze ETFs", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Placeholder for metrics table (will be populated later)
st.markdown("### ETF Performance Metrics")

# Sample data for layout demonstration
sample_data = {
    'Ticker': ['SPY', 'QQQ', 'IWM'],
    'Daily Return': ['0.02%', '0.03%', '0.01%'],
    'Weekly Return': ['0.15%', '0.18%', '0.12%'],
    'Monthly Return': ['0.65%', '0.72%', '0.58%']
}
df = pd.DataFrame(sample_data)

# Display metrics table with styling
st.dataframe(
    df.style.set_properties(**{
        'background-color': '#f8f9fa',
        'color': '#1E3D59',
        'border-color': '#dee2e6'
    })
)
