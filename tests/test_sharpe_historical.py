"""
Test script to compare Sharpe calculations using:
1. Latest rate fixed across all periods
2. Historical rates varying over time
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_test_data():
    """Get test ETF data and Treasury rates"""
    # Use SPY as test case
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)  # 2 years
    
    # Get SPY data
    spy = yf.Ticker("SPY")
    spy_data = spy.history(start=start_date)
    spy_returns = spy_data['Close'].pct_change().dropna()
    
    # Get ^IRX data with extended range to ensure we have data
    irx = yf.Ticker("^IRX")
    irx_data = irx.history(start=start_date - timedelta(days=30))  # Get extra month of data
    treasury_rates = irx_data['Close'] / 100  # Convert to decimal
    
    # Forward fill any missing values
    treasury_rates = treasury_rates.ffill().bfill()
    
    # Align dates with SPY returns
    treasury_rates = treasury_rates.reindex(spy_returns.index, method='ffill')
    
    return spy_returns, treasury_rates

def calculate_sharpe_latest_rate(returns, latest_rate):
    """Calculate Sharpe ratio using latest rate fixed for all periods"""
    daily_rf = latest_rate / 252
    excess_returns = returns - daily_rf
    if excess_returns.std() == 0:
        return 0
    return np.sqrt(252) * (excess_returns.mean() / excess_returns.std())

def calculate_sharpe_historical(returns, treasury_rates):
    """Calculate Sharpe ratio using historical rates"""
    # Align rates with returns and forward fill any gaps
    aligned_rates = treasury_rates.reindex(returns.index).ffill()
    daily_rf_rates = aligned_rates / 252
    excess_returns = returns - daily_rf_rates
    
    if excess_returns.std() == 0:
        return 0
    return np.sqrt(252) * (excess_returns.mean() / excess_returns.std())

def test_sharpe_calculations():
    """Compare Sharpe calculations using latest vs historical rates"""
    print("\nComparing Sharpe Ratio Calculations")
    print("-" * 50)
    
    # Get test data
    print("\n1. Fetching test data...")
    returns, treasury_rates = get_test_data()
    
    # Get latest rate
    latest_rate = treasury_rates.iloc[-1]
    print(f"\n2. Rate Information:")
    print(f"Latest Rate: {latest_rate:.5f} ({latest_rate*100:.5f}%)")
    print(f"Historical Rate Range: {treasury_rates.min():.5f} to {treasury_rates.max():.5f}")
    print(f"Historical Rate Mean: {treasury_rates.mean():.5f}")
    
    # Calculate Sharpe ratios
    print("\n3. Calculating Sharpe ratios...")
    latest_sharpe = calculate_sharpe_latest_rate(returns, latest_rate)
    historical_sharpe = calculate_sharpe_historical(returns, treasury_rates)
    
    print("\n4. Results Comparison:")
    print(f"Sharpe (Latest Rate {latest_rate*100:.5f}%): {latest_sharpe:.5f}")
    print(f"Sharpe (Historical Rates): {historical_sharpe:.5f}")
    print(f"Difference: {abs(historical_sharpe - latest_sharpe):.5f}")
    
    # Sample period analysis
    print("\n5. Sample Period Analysis (Last 5 Days):")
    sample_period = returns.index[-5:]
    
    for date in sample_period:
        print(f"\nDate: {date.date()}")
        daily_return = returns[date]
        hist_rate = treasury_rates.reindex([date]).iloc[0]
        
        print(f"ETF Return: {daily_return*100:.5f}%")
        print(f"Historical Rate: {hist_rate*100:.5f}%")
        print(f"Latest Rate: {latest_rate*100:.5f}%")
        
        # Daily excess returns
        excess_latest = daily_return - (latest_rate/252)
        excess_hist = daily_return - (hist_rate/252)
        
        print(f"Excess Return (Latest Rate): {excess_latest*100:.5f}%")
        print(f"Excess Return (Historical): {excess_hist*100:.5f}%")

if __name__ == "__main__":
    test_sharpe_calculations()
