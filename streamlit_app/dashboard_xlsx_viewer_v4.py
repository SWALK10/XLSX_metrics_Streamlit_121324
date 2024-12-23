#################################################################
# GLOBAL MODIFICATION RULE:                                           #
# Each section of working code is protected. ANY changes require:     #
# 1. Explicit approval from Scott                                    #
# 2. Changes discussed and approved one section at a time            #
# 3. Clear documentation of why the change is needed                 #
#################################################################

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path

# Add the src directory to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
from src.data.excel_manager import ExcelManager

# Constants from documentation
OUTPUT_DIR = os.path.join(project_root, "Test Output")

# Metrics Documentation
METRICS_DOC = """
### 📊 Calculation Methodology

#### Performance Metrics
- Returns calculated using adjusted close prices
- Daily: Current vs Previous Close
- Monthly: Last 30 calendar days
- YTD: From January 1st to current
- Annual: Calendar year returns (2023, 2022)

#### Risk & Performance
- Sharpe Ratio: 24-month rolling window
- Risk-Free Rate: 3% annual
- Calculation: (Avg Return - Risk Free Rate) / Std Dev

#### Dividend & Data
- Yield: Based on trailing 12-month dividends
- Data Source: Yahoo Finance API (daily updates)
- N/A: Insufficient data for calculation
- Colors: Green (positive) / Red (negative)
"""

#############################################################
# DO NOT MODIFY: Page Configuration and Styling Section START #
# Why Protected:                                             #
# - CSS styling carefully tuned for readability              #
# - Banner formatting optimized for different screen sizes   #
# - Table styles specifically matched to data formatting     #
#############################################################
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
###########################################################
# DO NOT MODIFY: Page Configuration and Styling Section END #
###########################################################

###################################################
# DO NOT MODIFY: Header Layout Section START       #
# Why Protected:                                   #
# - Layout ratios tested for optimal presentation  #
# - Logo placement and sizing optimized            #
# - Banner text styling matches brand guidelines   #
###################################################
# Create three columns for the header
left_col, center_col, right_col = st.columns([1, 2, 1])

# Empty left column for balance
with center_col:
    st.markdown("""
        <div class="banner">
            <h1>Financial Analysis Dashboard</h1>
            <h2>Walker Trading Partners</h2>
        </div>
    """, unsafe_allow_html=True)

# Logo in right column
with right_col:
    st.image("images/Logo_Final2_50pct.gif", width=150)
###############################################
# DO NOT MODIFY: Header Layout Section END    #
###############################################

################################################
# NEW SECTION: Ticker Input START              #
# Purpose: Allow user to filter ETFs to display #
################################################
# Create columns for ticker input
col1, col2 = st.columns([5,1])  
with col1:
    st.markdown("### Enter ETF Tickers")  
    ticker_input = st.text_input(
        "",  
        placeholder="Enter comma-separated tickers (e.g., SPY, QQQ, IWM)",
        label_visibility="collapsed"  
    )
with col2:
    st.write("")  
    st.write("")  
    analyze_button = st.button("Analyze ETFs")  

# Process ticker input
tickers = [t.strip().upper() for t in ticker_input.split(',')] if ticker_input else []

# When Analyze is clicked, fetch new data
if analyze_button and tickers:
    with st.spinner("Downloading and processing ETF data..."):
        try:
            # Initialize ExcelManager following documentation flow
            excel_mgr = ExcelManager(OUTPUT_DIR, tickers)
            
            success = True
            for ticker in tickers:
                # Follow documented data flow steps
                adj_prices, unadj_prices, dividends = excel_mgr.download_ticker_data(ticker)
                if adj_prices is not None:
                    if not excel_mgr.save_ticker_data(ticker, adj_prices, unadj_prices, dividends):
                        success = False
                        st.error(f"Failed to save data for {ticker}")
                        break
                else:
                    success = False
                    st.error(f"Failed to download data for {ticker}")
                    break
            
            if success:
                excel_path = excel_mgr.excel_path
                st.success("Data updated successfully!")
            else:
                excel_path = None
        except Exception as e:
            st.error(f"Error in data processing flow: {str(e)}")
            excel_path = None
else:
    # Find latest file following naming convention from docs
    try:
        excel_files = [f for f in os.listdir(OUTPUT_DIR) 
                      if f.startswith("dashboard_data_") and f.endswith(".xlsx")]
        if excel_files:
            latest_file = max(excel_files)  # Uses timestamp in filename for ordering
            excel_path = os.path.join(OUTPUT_DIR, latest_file)
        else:
            st.warning("No existing data files found. Please enter tickers and click Analyze.")
            excel_path = None
    except Exception as e:
        st.error(f"Error accessing data directory: {str(e)}")
        excel_path = None
##############################################
# NEW SECTION: Ticker Input END             #
##############################################

# Add metrics documentation expander
with st.expander("📝 Notes & Methodology"):
    st.markdown(METRICS_DOC)

#################################################
# DO NOT MODIFY: Core Functions Section START    #
# Why Protected:                                 #
# - ETF name shortening logic tested extensively #
# - Color coding logic handles all edge cases    #
# - Functions used by multiple dashboard parts   #
#################################################
def shorten_etf_name(name):
    """Smart ETF name shortening"""
    # Remove common suffixes
    name = name.replace(" ETF", "").replace(" Trust", "")
    
    # Special cases for different types
    if "Treasury Bond" in name:
        name = name.replace("Treasury Bond", "Treasury")
    if "Year" in name:
        name = name.replace("Year", "Y")
        
    return name

def style_negative_red(val):
    """Color negative values red and positive values green"""
    try:
        if isinstance(val, str):
            return ''
        color = 'red' if float(val) < 0 else 'green'
        return f'color: {color}'
    except:
        return ''
###############################################
# DO NOT MODIFY: Core Functions Section END   #
###############################################

try:
    # Read the test Excel file
    df = pd.read_excel(excel_path, sheet_name='Metrics')
    
    # Filter by tickers if provided
    if tickers:
        df = df[df['Ticker'].isin(tickers)]
    
    # Shorten ETF names
    df['Name'] = df['Name'].apply(shorten_etf_name)
    
    # Define columns
    pct_columns = ['%Yield', 'Day%', 'MTD%', 'YTD%', '2023%', '2022%', 'Volatility', 'Max_Drawdown']
    
    # Multiply percentage columns by 100
    for col in pct_columns:
        df[col] = df[col] * 100
    
    # Simple tab selection
    tab1, tab2 = st.tabs(["Metrics", "Correlation Analysis"])
    
    with tab1:
        # Add back the ETF Metrics title
        st.markdown("### ETF Metrics")
        
        if df.empty and tickers:
            st.warning("No data found for the specified tickers")
        else:
            ########################################################
            # DO NOT MODIFY: Table Formatting Section START         #
            # Why Protected:                                        #
            # - Number formatting optimized for readability         #
            # - Column widths carefully balanced                    #
            # - Color coding tested with all data scenarios        #
            # - Percentage handling verified with edge cases        #
            ########################################################
            # Apply styling to the dataframe
            styled_df = df.style.applymap(
                style_negative_red, 
                subset=pct_columns + ['Sharpe']
            )
            
            # Display with Streamlit - Specific column formatting
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
            ######################################################
            # DO NOT MODIFY: Table Formatting Section END         #
            ######################################################
    
    with tab2:
        st.write("### Correlation Analysis")
        st.write("(Placeholder for future correlation heatmap)")

except Exception as e:
    st.error(f"Error reading Excel file: {str(e)}")
    st.write("Full error:", e)
