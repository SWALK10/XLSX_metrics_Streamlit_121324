import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="Financial Analysis Dashboard", layout="wide")

# Custom CSS for the banner and table styling
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
    .logo-placeholder {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        color: #666;
        height: 100px;
        width: 100px;
        line-height: 80px;
        margin: 0 auto;
        position: relative;
        top: -20px;
    }
    /* Make table content larger */
    .stDataFrame td {
        font-size: 1.15em !important;
    }
    /* Center align numeric columns */
    .stDataFrame th:nth-child(n+3) {
        text-align: center !important;
    }
    /* Adjust button alignment */
    .stButton {
        margin-top: 1.7em;
    }
    </style>
""", unsafe_allow_html=True)

# Create three columns for layout
col1, col2, col3 = st.columns([1, 2, 1])

# Add logo to the right column
with col3:
    st.image("images/Logo_Final2_50pct.gif", width=150)

# Add title to the middle column
with col2:
    st.markdown('<div class="banner"><h1>Financial Analysis Dashboard</h1><h2>Walker Trading Partners</h2></div>', unsafe_allow_html=True)

def shorten_etf_name(name):
    """Smart ETF name shortening"""
    # Remove common words
    remove_words = ['SPDR', 'iShares', 'Vanguard', 'ETF', 'Fund', 'Trust']
    for word in remove_words:
        name = name.replace(word, '').strip()
    # Remove extra spaces
    name = ' '.join(name.split())
    return name

def read_existing_metrics(tickers_input: str = None) -> pd.DataFrame:
    """Only reads from existing XLSX files, no data generation"""
    try:
        # Find most recent XLSX file in directory
        base_path = "S:/Dropbox/Scott Only Internal/Quant_Python_24/Basic_XLSX_PlusCalc_Restored_120424/test_output"
        xlsx_files = [f for f in os.listdir(base_path) if f.endswith('.xlsx')]
        if not xlsx_files:
            st.error("No existing XLSX files found")
            return None
            
        latest_file = max(xlsx_files, key=lambda x: os.path.getmtime(os.path.join(base_path, x)))
        
        # Read metrics from existing file
        df = pd.read_excel(
            os.path.join(base_path, latest_file),
            sheet_name='Metrics'
        )
        
        # Filter for requested tickers if provided
        if tickers_input:
            tickers = [t.strip().upper() for t in tickers_input.split(',')]
            df = df[df['Ticker'].isin(tickers)]
            
        return df
        
    except Exception as e:
        st.error(f"Error reading metrics: {str(e)}")
        return None

def style_negative_red(val):
    """Color negative values red and positive values green"""
    try:
        if isinstance(val, str):
            val = float(val.strip('%'))
        if pd.isna(val):
            return ''
        color = 'red' if val < 0 else 'green'
        return f'color: {color}'
    except:
        return ''

# Add tabs
tab1, tab2 = st.tabs(["Metrics", "Correlation Analysis"])

with tab1:
    # Add ticker input
    st.markdown("### Enter ETF Tickers")
    col1, col2 = st.columns([4, 1])
    with col1:
        tickers = st.text_input("Enter comma-separated tickers (e.g., SPY, QQQ, IWM)", key="tickers")
    with col2:
        analyze_button = st.button("Analyze ETFs")

    if analyze_button or not tickers:  # Show all data if no tickers entered
        with st.spinner("Loading ETF metrics..."):
            df = read_existing_metrics(tickers if tickers else None)
            
            if df is not None and not df.empty:
                # Shorten ETF names
                df['Name'] = df['Name'].apply(shorten_etf_name)
                
                # Format percentage columns
                pct_columns = ['%Yield', 'Day%', 'MTD%', 'YTD%', '2023%', '2022%', 'Volatility', 'Max_Drawdown']
                for col in pct_columns:
                    df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "")
                
                # Format Sharpe ratio
                df['Sharpe'] = df['Sharpe'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")
                
                # Apply styling
                styled_df = df.style.applymap(
                    style_negative_red, 
                    subset=pct_columns + ['Sharpe']
                )
                
                # Display the table
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    column_config={
                        'Ticker': st.column_config.TextColumn('Ticker', width='small'),
                        'Name': st.column_config.TextColumn('Name'),
                        'Sharpe': st.column_config.NumberColumn('Sharpe', format='%.2f'),
                        **{col: st.column_config.NumberColumn(col, format='%.1f%%') 
                           for col in pct_columns}
                    },
                    hide_index=True
                )
            elif df is not None:
                st.warning("No data found for specified tickers")

with tab2:
    st.markdown("### Correlation Analysis")
    st.info("Correlation analysis will be implemented in the next phase")
