"""
Test script to check Treasury rate availability in yfinance
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def test_treasury_data():
    # Treasury tickers to test
    tickers = [
        "^IRX",  # 13-week Treasury Bill
        "ZN=F",  # 10-Year T-Note Futures
        "SHY",   # 1-3 Year Treasury Bond ETF
        "BIL",   # 1-3 Month Treasury Bill ETF
    ]
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    print("Testing Treasury rate data availability:")
    print("-" * 50)
    
    for ticker in tickers:
        try:
            treasury = yf.Ticker(ticker)
            hist = treasury.history(start=start_date, end=end_date)
            info = treasury.info
            print(f"\nTicker: {ticker}")
            print(f"Data points: {len(hist)}")
            print(f"Latest close: {hist['Close'].iloc[-1]:.2f}")
            if 'yield' in info:
                print(f"Current yield: {info['yield']:.2f}%")
            print(f"Available info keys: {list(info.keys())[:5]}...")
            
            # Show last 5 days for SHY
            if ticker == "SHY":
                print("\nLast 5 days of SHY (1-3 Year Treasury ETF):")
                print(hist['Close'].tail().to_string())
                
        except Exception as e:
            print(f"\nError with {ticker}: {str(e)}")

if __name__ == "__main__":
    test_treasury_data()
