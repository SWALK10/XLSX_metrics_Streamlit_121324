"""
Test NA handling in Excel output using existing ExcelManager
"""
import os
import sys
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.data.excel_manager import ExcelManager

def test_na_handling():
    # Test directory
    test_dir = os.path.join(project_root, "Test Output")
    os.makedirs(test_dir, exist_ok=True)
    
    # Test with problematic tickers
    test_tickers = ['ISPY', 'SVOL', 'SPY']
    
    # Initialize Excel Manager
    excel_mgr = ExcelManager(test_dir, test_tickers)
    
    # Process each ticker
    for ticker in test_tickers:
        # Download data
        adj_prices, unadj_prices, dividends = excel_mgr.download_ticker_data(ticker)
        if adj_prices is not None:
            # Save to Excel
            excel_mgr.save_ticker_data(ticker, adj_prices, unadj_prices, dividends)
    
    print(f"Test complete. Output file: {excel_mgr.excel_path}")

if __name__ == "__main__":
    test_na_handling()
