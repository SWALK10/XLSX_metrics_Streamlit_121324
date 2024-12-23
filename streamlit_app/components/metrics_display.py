"""
Metrics display component for the Streamlit dashboard
"""
import streamlit as st
import pandas as pd

def display_metrics(excel_file: str):
    """
    Display metrics from the Excel file in a formatted table
    """
    try:
        # Read metrics sheet
        df = pd.read_excel(excel_file, sheet_name='Metrics')
        
        # Format the display
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                col: st.column_config.NumberColumn(
                    col,
                    format="%.2f%%"
                ) for col in df.columns if 'return' in col.lower() or 'yield' in col.lower()
            }
        )
        
        return True
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
        return False
