"""
Test script for Excel NA handling
"""
import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data.excel_manager_test import run_test
from src.models.metrics_test import calculate_all_ticker_metrics
import pandas as pd

# Test directory
TEST_OUTPUT_DIR = "S:/Dropbox/Scott Only Internal/Quant_Python_24/XLSX_metrics_Streamlit_121324/Test Output"

# Test with the problematic tickers
test_tickers = ['ISPY', 'SVOL', 'SPY']

if __name__ == "__main__":
    print("Running Excel NA handling test...")
    
    # First write the price data
    output_file = run_test(test_tickers, TEST_OUTPUT_DIR)
    print(f"Price data written to: {output_file}")
    
    # Now calculate and write metrics
    try:
        # Read the price data
        price_df = pd.read_excel(output_file, sheet_name='Daily Prices', index_col=0)
        
        # Calculate metrics
        metrics_df = calculate_all_ticker_metrics(price_df)
        
        # Write metrics to new sheet
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='a') as writer:
            metrics_df.to_excel(
                writer,
                sheet_name='Metrics',
                index=False,
                na_rep='#N/A'
            )
        print("Metrics calculation complete and written to Excel")
        
    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
