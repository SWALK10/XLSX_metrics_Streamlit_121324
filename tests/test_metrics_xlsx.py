# test_metrics_xlsx.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import yfinance as yf
from src.data.excel_manager import ExcelManager
from datetime import datetime

def run_test():
    # Test with a single ticker
    tickers = ['SPY']  # Start with just one ticker
    data_dir = "Test Output"
    
    # Initialize Excel Manager
    excel_mgr = ExcelManager(data_dir, tickers)
    
    # Download and save data
    for ticker in tickers:
        print(f"\nProcessing {ticker}...")
        adj_prices, unadj_prices, dividends = excel_mgr.download_ticker_data(ticker)
        if adj_prices is not None:
            print(f"Got price data for {ticker}, saving...")
            success = excel_mgr.save_ticker_data(ticker, adj_prices, unadj_prices, dividends)
            print(f"Save {'successful' if success else 'failed'} for {ticker}")
        else:
            print(f"Failed to get data for {ticker}")

if __name__ == "__main__":
    run_test()
