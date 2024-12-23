"""
Test script to verify ETF data capture and metrics calculation for SPY, JNK, IEI
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data.excel_manager import ExcelManager

def main():
    # Use the specified output directory
    output_dir = r"S:\Dropbox\Scott Only Internal\Quant_Python_24\Basic_XLSX_PlusCalc_Restored_120424\test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Writing to directory: {output_dir}")
    tickers = ['SPY', 'JNK', 'IEI']
    manager = ExcelManager(output_dir, tickers)
    
    for ticker in tickers:
        print(f"\nDownloading {ticker} data...")
        adj_prices, unadj_prices, dividends = manager.download_ticker_data(ticker)
        
        # Try to save the data
        print(f"\nAttempting to save {ticker} data...")
        save_success = manager.save_ticker_data(ticker, adj_prices, unadj_prices, dividends)
        if not save_success:
            print(f"\nWARNING: Failed to save {ticker} data to Excel. Please ensure the file is not open.")
        
        # Print summary
        print(f"\n{ticker} Data Summary:")
        print(f"Adjusted Prices: {len(adj_prices)} records from {adj_prices.index[0]} to {adj_prices.index[-1]}")
        print(f"Unadjusted Prices: {len(unadj_prices)} records from {unadj_prices.index[0]} to {unadj_prices.index[-1]}")
        print(f"\nDividend Records ({len(dividends)}):")
        if not dividends.empty:
            print("\nLast 5 dividends:")
            print(dividends.sort_index(ascending=False).head())  # Show last 5 dividends
    
    print(f"\nOutput file: {manager.excel_path}")
    print(f"Save status: {'Success' if save_success else 'Failed'}")
    print("\nCheck the 'Metrics' sheet in the Excel file for calculated metrics.")

if __name__ == '__main__':
    main()
