"""
Simple test script to display metrics from existing Excel file
"""
import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="ETF Metrics Display Test", layout="wide")

# Title
st.title("ETF Metrics Display Test")

# Specify the exact file we know works
EXCEL_FILE = "S:/Dropbox/Scott Only Internal/Quant_Python_24/Git_Restore_XLSX_Calc_121124/Test Output/dashboard_data_20241213_1950.xlsx"

try:
    # Read the Metrics sheet
    df = pd.read_excel(EXCEL_FILE, sheet_name='Metrics')
    
    # Display basic info about the data
    st.write("### Data Overview")
    st.write(f"Number of metrics: {len(df.columns)}")
    st.write(f"Number of tickers: {len(df)}")
    
    # Display the metrics table
    st.write("### Metrics Table")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            col: st.column_config.NumberColumn(
                col,
                format="%.2f%" if 'return' in col.lower() or 'yield' in col.lower() else "%.2f"
            ) for col in df.columns
        }
    )
    
    # Show the raw data (for debugging)
    if st.checkbox("Show raw data"):
        st.write("### Raw Data")
        st.write(df)

except Exception as e:
    st.error(f"Error reading Excel file: {str(e)}")
    st.write("Error details:", e)
