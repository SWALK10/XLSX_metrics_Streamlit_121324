"""
ETF Analytics Dashboard
"""
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# Import project modules
try:
    from streamlit_app.components.metrics_display import display_metrics
    from streamlit_app.components.charts import plot_price_history
    from streamlit_app.utils.excel_reader import get_latest_excel, get_file_info
except ImportError as e:
    logger.error(f"Failed to import local modules: {e}")
    st.error("Failed to initialize required components. Please check the application setup.")
    sys.exit(1)

# Import the test module
try:
    sys.path.append(os.path.join(ROOT_DIR, 'tests'))
    from test_etf_data_w_metrics import main as run_etf_analysis
except ImportError as e:
    logger.error(f"Failed to import test module: {e}")
    st.error("Failed to initialize analysis module. Please check the application setup.")
    sys.exit(1)

# Page config
try:
    st.set_page_config(
        page_title="ETF Analytics Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    logger.error(f"Failed to set page config: {e}")
    st.error("Failed to initialize page configuration.")
    sys.exit(1)

# Custom CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .reportview-container {
        background: #f0f2f6
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("ETF Analytics Dashboard")
st.markdown("---")

# Sidebar for inputs
with st.sidebar:
    st.header("Analysis Parameters")
    
    # Ticker input
    ticker_input = st.text_area(
        "Enter Ticker Symbols (one per line)",
        value="SPY\nJNK\nIEI",
        height=100,
        help="Enter each ticker symbol on a new line"
    )
    
    # Run analysis button
    if st.button("Run Analysis", type="primary"):
        tickers = [t.strip() for t in ticker_input.split('\n') if t.strip()]
        st.session_state['tickers'] = tickers
        
        with st.spinner("Running analysis..."):
            try:
                run_etf_analysis()
                st.success("Analysis complete!")
            except Exception as e:
                logger.error(f"Analysis failed: {e}")
                st.error(f"Error during analysis: {str(e)}")

# Main content area
try:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Price History")
        latest_file = get_latest_excel("Test Output")
        if latest_file:
            plot_price_history(latest_file)
        else:
            st.info("No price data available. Please run an analysis first.")

    with col2:
        st.header("ETF Metrics")
        if latest_file:
            display_metrics(latest_file)
            
            # Show file info
            file_name, creation_time = get_file_info(latest_file)
            st.caption(f"Last updated: {creation_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.info("No metrics available. Please run an analysis first.")
except Exception as e:
    logger.error(f"Failed to render main content: {e}")
    st.error("Error displaying dashboard content. Please check the logs for details.")

# Footer
st.markdown("---")
st.caption("ETF Analytics Dashboard - Data updates when analysis is run")
