# Copy of v4 with logo path fix
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
LOGO_PATH = os.path.join(project_root, "streamlit_app", "images", "Logo_Final2_50pct.gif")

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
    st.image(LOGO_PATH, width=150)
###############################################
# DO NOT MODIFY: Header Layout Section END    #
###############################################

################################################
# DO NOT MODIFY: User Input Section START        #
# Why Protected:                                 #
# - Input validation carefully implemented       #
# - Error handling for invalid tickers in place  #
# - Layout optimized for usability               #
################################################
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

if analyze_button and tickers:
    with st.spinner("Downloading and processing ETF data..."):
        try:
            # Initialize ExcelManager following documentation flow
            excel_mgr = ExcelManager(OUTPUT_DIR, tickers)
            
            # Download and process data
            excel_mgr.download_data()
            excel_mgr.calculate_metrics()
            excel_mgr.write_to_excel()
            
            st.success("Data processed successfully!")
            
        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.stop()

###############################################
# DO NOT MODIFY: User Input Section END       #
###############################################

###############################################
# DO NOT MODIFY: Core Functions Section START #
# Why Protected:                             #
# - Name shortening logic tested extensively #
# - Color coding matches Excel exactly       #
###############################################
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
        val = float(str(val).strip('%'))
        if val < 0:
            return 'color: red'
        return 'color: green'
    except:
        return ''
###############################################
# DO NOT MODIFY: Core Functions Section END   #
###############################################

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
    
    # Format the dataframe
    df['Name'] = df['Name'].apply(shorten_etf_name)
    
    # Define columns that should be formatted as percentages
    pct_columns = ['Day%', 'MTD%', 'YTD%', '2023%', '2022%', 'Volatility', 'Max_Drawdown', '%Yield']
    
    # Apply percentage formatting
    for col in pct_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:.1f}%" if pd.notnull(x) else "")
    
    # Format Sharpe ratio
    if 'Sharpe' in df.columns:
        df['Sharpe'] = df['Sharpe'].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Metrics", "🔄 Correlation"])
    
    with tab1:
        # Apply styling to the dataframe
        styled_df = df.style.applymap(
            style_negative_red, 
            subset=pct_columns + ['Sharpe']
        )
        
        # Display the styled dataframe
        st.dataframe(
            styled_df,
            hide_index=True,
            use_container_width=True
        )
    
    with tab2:
        st.info("Correlation analysis coming soon!")

except Exception as e:
    st.error(f"Error reading data: {str(e)}")
