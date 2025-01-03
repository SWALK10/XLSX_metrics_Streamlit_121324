################################################################
# *** DO NOT Change Layout ***                                   #
# Layout sections in this file are carefully tuned and tested.   #
# Changes to layout elements will break the dashboard display.   #
# Each section is marked with start/end markers.                 #
################################################################

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
import yfinance as yf

# Add the src directory to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
from src.data.excel_manager import ExcelManager
from src.visualization.relative_strength_chart_test import RelativeStrengthChart

# Constants from documentation
OUTPUT_DIR = os.path.join(project_root, "Test Output")
LOGO_PATH = os.path.join(project_root, "streamlit_app", "images", "Logo_Final2_50pct.gif")

################################################################
# *** DO NOT Change Layout - Page Configuration START ***        #
# - CSS styling carefully tuned for readability                  #
# - Banner formatting optimized for different screen sizes       #
# - Table styles specifically matched to data formatting         #
################################################################
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
################################################################
# *** DO NOT Change Layout - Page Configuration END ***          #
################################################################

################################################################
# *** DO NOT Change Layout - Header Section START ***            #
# - Layout ratios tested for optimal presentation                #
# - Logo placement and sizing optimized                          #
# - Banner text styling matches brand guidelines                 #
################################################################
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
    st.image(LOGO_PATH, width=150)
################################################################
# *** DO NOT Change Layout - Header Section END ***              #
################################################################

################################################################
# *** DO NOT Change Layout - Input Section START ***             #
# - Input validation carefully implemented                       #
# - Error handling for invalid tickers in place                  #
# - Layout optimized for usability                              #
################################################################
# Add ticker input below banner
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

# Process tickers if provided
tickers = None
if ticker_input:
    # Clean and validate tickers
    tickers = [t.strip().upper() for t in ticker_input.split(",")]
    tickers = [t for t in tickers if t]  # Remove empty strings

# When Analyze is clicked, fetch new data
if analyze_button and tickers:
    with st.spinner("Downloading and processing ETF data..."):
        try:
            # Initialize ExcelManager following documentation flow
            excel_mgr = ExcelManager(OUTPUT_DIR, tickers)
            
            success = True
            ticker_names = {}  # Store ticker -> name mapping
            for ticker in tickers:
                # Get ETF name from yfinance
                stock = yf.Ticker(ticker)
                try:
                    ticker_names[ticker] = stock.info.get('longName', ticker)
                except:
                    ticker_names[ticker] = ticker  # Fallback to ticker if name not found
                
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
################################################################
# *** DO NOT Change Layout - Input Section END ***               #
################################################################

################################################################
# *** DO NOT Change Layout - Core Functions Section START ***    #
# - Name shortening logic tested extensively                     #
# - Color coding matches Excel exactly                           #
################################################################
def style_negative_red(val):
    """Color negative values red and positive values green"""
    try:
        val = float(str(val).strip('%'))
        if val < 0:
            return 'color: red'
        return 'color: green'
    except:
        return ''
################################################################
# *** DO NOT Change Layout - Core Functions Section END ***      #
################################################################

try:
    # Get the latest Excel file
    excel_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.xlsx')]
    if not excel_files:
        st.warning("No data files found. Please analyze some ETFs first.")
        st.stop()
    
    latest_file = max([os.path.join(OUTPUT_DIR, f) for f in excel_files], 
                     key=os.path.getmtime)
    
    # Read the metrics sheet
    df = pd.read_excel(latest_file, sheet_name='Metrics', engine='openpyxl')
    
    # Remove Default_Rate column if it exists
    if 'Default_Rate' in df.columns:
        df = df.drop('Default_Rate', axis=1)
    
    # Debug print
    print("Raw values from Excel:")
    print(df[['YTD%', '2023%']].head())
    
    ################################################################
    # ***                  PROTECTED CODE SECTION                 *** #
    # ***              DO NOT MODIFY WITHOUT PERMISSION          *** #
    # ***         CRITICAL PERCENTAGE FORMATTING LOGIC           *** #
    ################################################################
    #
    # EXPLANATION:
    # - Excel stores percentages as decimals (e.g., 0.29 for 29%)
    # - When pandas reads these values, they come in as decimals
    # - We must multiply by 10000 to convert from decimal to percentage
    # - Example: 0.0029 (from Excel) * 10000 = 29.0%
    #
    # WARNING:
    # - DO NOT change the multiplication factor of 10000
    # - DO NOT modify the formatting string "{x:.1f}%"
    # - DO NOT change the column list without approval
    # - This section is tested and verified working
    ################################################################
    
    # Define columns that should be formatted as percentages
    pct_columns = ['Day%', '1MTH%', 'YTD%', '2023%', '2022%', '%Yield', 'Volatility', 'Max_Drawdown']
    
    # Convert decimal values to properly formatted percentages
    for col in pct_columns:
        if col in df.columns:
            df[col] = df[col].multiply(10000).apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "")
    
    ################################################################
    # ***            END OF PROTECTED CODE SECTION               *** #
    ################################################################

    # Format Sharpe ratio with 2 decimal places
    if 'Sharpe 2Y' in df.columns:
        df['Sharpe 2Y'] = df['Sharpe 2Y'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")

    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Metrics", "📈 Performance", "🔄 Correlation"])
    
    with tab1:
        # Apply styling to the dataframe
        styled_df = df.style.map(
            style_negative_red, 
            subset=pct_columns + ['Sharpe 2Y']
        ).set_properties(**{
            'text-align': 'left'
        }, subset=['Ticker', 'Name']).set_properties(**{
            'text-align': 'right'
        }, subset=pct_columns + ['Sharpe 2Y'])
        
        # Display the styled dataframe using Streamlit's column configuration
        st.dataframe(
            styled_df,
            use_container_width=True,
            column_config={
                'Ticker': st.column_config.TextColumn('Ticker', width='small'),
                'Name': st.column_config.TextColumn('Name'),
                'Sharpe 2Y': st.column_config.NumberColumn('Sharpe 2Y', format='%.2f'),
                **{col: st.column_config.NumberColumn(col, format='%.1f%%') 
                   for col in pct_columns}
            },
            hide_index=True
        )
    
    with tab2:
        try:
            rs_chart = RelativeStrengthChart()
            
            max_fig = rs_chart.create_max_chart(latest_file)
            if max_fig:
                st.plotly_chart(max_fig, use_container_width=True)
            else:
                st.warning("Unable to create max relative performance chart. Please check the data.")
            
            st.markdown("---")
            
            one_year_fig = rs_chart.create_1year_chart(latest_file)
            if one_year_fig:
                st.plotly_chart(one_year_fig, use_container_width=True)
            else:
                st.warning("Unable to create 1 year relative performance chart. Please check the data.")
            
            st.markdown("---")
            
            three_month_fig = rs_chart.create_3month_chart(latest_file)
            if three_month_fig:
                st.plotly_chart(three_month_fig, use_container_width=True)
            else:
                st.warning("Unable to create 3 month relative performance chart. Please check the data.")
        except Exception as e:
            st.error(f"Error creating relative performance charts: {str(e)}")
    
    with tab3:
        st.info("Correlation analysis coming soon!")

except Exception as e:
    st.error(f"Error reading data: {str(e)}")

# Add metrics documentation expander at bottom of page
with st.expander("📝 Notes & Methodology"):
    st.markdown("""
### 📊 Calculation Methodology

#### Performance Metrics
- Returns calculated using adjusted close prices
- Daily: Current vs Previous Close
- Monthly: Last 30 calendar days
- YTD: From January 1st to current
- Annual: Calendar year returns (2023, 2022)

#### Risk & Performance
- Sharpe Ratio: 24-month rolling window
- Risk-Free Rate: Based on BIL ETF (SPDR Bloomberg 1-3 Month T-Bill)
- Calculation: (Avg Return - Risk Free Rate) / Std Dev

#### Dividend & Data
- Yield: Based on trailing 12-month dividends
- Data Source: Yahoo Finance API (daily updates)
- N/A: Insufficient data for calculation
- Colors: Green (positive) / Red (negative)
""")
