import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / 'src'
sys.path.append(str(src_path))

# Import our existing modules
from data.stock_fetcher import StockFetcher
from models.performance_metrics import PerformanceMetrics

# Set page config
st.set_page_config(page_title="Live ETF Analysis Dashboard", layout="wide")

def process_ticker_input(ticker_string: str):
    """Process comma-separated ticker input"""
    if not ticker_string:
        return []
    # Split and clean tickers
    tickers = [t.strip().upper() for t in ticker_string.split(',')]
    return tickers

def main():
    st.title("Live ETF Analysis Dashboard")
    
    # Ticker input section
    st.subheader("Enter ETF Tickers")
    ticker_input = st.text_input(
        "Enter comma-separated tickers (e.g., SPY, QQQ, IWM)",
        help="Enter ETF tickers separated by commas"
    )
    
    if st.button("Analyze ETFs"):
        if ticker_input:
            tickers = process_ticker_input(ticker_input)
            
            with st.spinner('Fetching data and calculating metrics...'):
                try:
                    # Initialize our existing components
                    fetcher = StockFetcher()
                    metrics_calculator = PerformanceMetrics()
                    
                    # Fetch data and calculate metrics
                    results = []
                    for ticker in tickers:
                        data = fetcher.get_stock_data(ticker)
                        if data is not None:
                            metrics = metrics_calculator.calculate_all_metrics(data)
                            results.append({
                                'Ticker': ticker,
                                **metrics
                            })
                        else:
                            st.warning(f"Could not fetch data for {ticker}")
                    
                    if results:
                        # Convert to DataFrame and display
                        df = pd.DataFrame(results)
                        st.dataframe(df)
                    else:
                        st.error("No valid data found for any of the provided tickers")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter at least one ticker")

if __name__ == "__main__":
    main()
