"""
Test script for Treasury rate CSV handling
Tests ^IRX historical data fetching and CSV operations without timestamps
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path

def setup_data_dir():
    """Create data directory if it doesn't exist"""
    data_dir = Path("data/treasury_rates")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_irx_history(start_date):
    """
    Fetch ^IRX rate history from start_date
    Args:
        start_date: datetime object for start of history
    """
    try:
        irx = yf.Ticker("^IRX")
        data = irx.history(start=start_date)
        if not data.empty:
            # Convert percentage to decimal (e.g., 4.22% -> 0.0422)
            rates = data['Close'] / 100
            return pd.DataFrame({
                'date': rates.index.date,
                'rate': rates.values
            })
    except Exception as e:
        print(f"Error fetching ^IRX history: {e}")
    return None

def save_rates_to_csv(rates_df, csv_path):
    """Save historical rates to CSV"""
    rates_df.to_csv(csv_path, index=False)
    return True

def test_treasury_history():
    """Test historical rate fetching"""
    print("\nTesting Treasury Rate Historical Data")
    print("-" * 50)
    
    # Setup
    data_dir = setup_data_dir()
    csv_path = data_dir / "daily_rates.csv"
    
    # Calculate start date (2 years ago for Sharpe)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)  # 2 years of data
    
    # 1. Test historical ^IRX fetch
    print(f"\n1. Fetching ^IRX history from {start_date.date()}...")
    rates_df = get_irx_history(start_date)
    if rates_df is not None:
        print(f"Fetched {len(rates_df)} days of rates")
        print("\nFirst 5 days:")
        print(rates_df.head().to_string())
        print("\nLast 5 days:")
        print(rates_df.tail().to_string())
    else:
        print("Failed to fetch historical rates")
        return
    
    # 2. Test CSV save
    print("\n2. Saving to CSV...")
    if save_rates_to_csv(rates_df, csv_path):
        print(f"Historical rates saved to {csv_path}")
    
    # 3. Verify data continuity
    print("\n3. Checking data continuity...")
    dates = pd.to_datetime(rates_df['date'])
    gaps = (dates.diff() > pd.Timedelta(days=1)).sum()
    print(f"Number of gaps in data: {gaps}")
    
    # 4. Display date range statistics
    print("\n4. Date Range Summary:")
    print(f"Start Date: {rates_df['date'].min()}")
    print(f"End Date: {rates_df['date'].max()}")
    print(f"Total Days: {len(rates_df)}")

if __name__ == "__main__":
    test_treasury_history()
