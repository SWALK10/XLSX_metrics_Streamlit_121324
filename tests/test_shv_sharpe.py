"""
Quick test script to calculate SHV 1-year Sharpe ratio
Uses adjusted close prices
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def test_shv_sharpe():
    """Calculate SHV 1-year Sharpe ratio with detailed output"""
    try:
        # Get current date for 1-year lookback
        end_date = datetime.now()
        start_date = end_date - timedelta(days=400)  # Get extra days for calculations
        
        # Fetch SHV data with adjusted close prices
        shv = yf.Ticker("SHV")
        prices = shv.history(start=start_date, end=end_date, auto_adjust=True)['Close']
        returns = prices.pct_change().dropna()
        returns = returns[-252:]  # Get exactly 1 year of data
        
        # Print date range
        print("\nDate Range for Sharpe Calculation:")
        print(f"Start Date: {returns.index[0].strftime('%Y-%m-%d')}")
        print(f"End Date: {returns.index[-1].strftime('%Y-%m-%d')}")
        print(f"Number of trading days: {len(returns)}")
        
        # Use constant 5% risk-free rate for testing
        rf_rates = pd.Series(0.05, index=returns.index)  # 5% annual rate
        
        # Print intermediate values
        print("\nIntermediate Values:")
        print(f"Average Daily Return: {returns.mean():.6f}")
        print(f"Return Std Dev: {returns.std():.6f}")
        print(f"Annual Risk-Free Rate: 5.00%")
        
        # Calculate daily excess returns
        daily_rf = rf_rates / 252
        excess_returns = returns - daily_rf
        
        print(f"Average Daily Excess Return: {excess_returns.mean():.6f}")
        print(f"Excess Return Std Dev: {excess_returns.std():.6f}")
        
        # Calculate Sharpe ratio using daily metrics first
        daily_sharpe = excess_returns.mean() / excess_returns.std()
        
        # Annualize the ratio
        sharpe = daily_sharpe * np.sqrt(252)
        
        print(f"\nCalculated Sharpe Ratio: {sharpe:.2f}")
        
    except Exception as e:
        print(f"Error in test calculation: {str(e)}")

if __name__ == "__main__":
    test_shv_sharpe()
