"""
Detailed analysis of SHV Sharpe ratio calculation
Breaks down each step to identify potential issues
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_shv_sharpe():
    print("\nAnalyzing SHV Sharpe Ratio Components")
    print("-" * 50)
    
    # Constants
    TRADING_DAYS_YEAR = 252
    
    # 1. Get SHV data for last 2 years
    print("\n1. Fetching SHV Data...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)
    
    shv = yf.Ticker("SHV")
    shv_data = shv.history(start=start_date)
    shv_returns = shv_data['Close'].pct_change().dropna()
    
    print(f"Number of return data points: {len(shv_returns)}")
    print(f"Average Daily Return: {shv_returns.mean()*100:.5f}%")
    print(f"Return Std Dev (Daily): {shv_returns.std()*100:.5f}%")
    print(f"Annualized Volatility: {shv_returns.std() * np.sqrt(TRADING_DAYS_YEAR)*100:.5f}%")
    
    # 2. Get Treasury rates
    print("\n2. Fetching Treasury Rates...")
    irx = yf.Ticker("^IRX")
    irx_data = irx.history(start=start_date - timedelta(days=30))
    treasury_rates = irx_data['Close'] / 100
    treasury_rates = treasury_rates.ffill().bfill()
    
    # Align rates with SHV returns
    aligned_rates = treasury_rates.reindex(shv_returns.index, method='ffill')
    daily_rf_rates = aligned_rates / TRADING_DAYS_YEAR
    
    print(f"Average Daily Risk-Free Rate: {daily_rf_rates.mean()*100:.5f}%")
    print(f"Current Risk-Free Rate (Annual): {aligned_rates.iloc[-1]*100:.2f}%")
    
    # 3. Calculate excess returns
    print("\n3. Analyzing Excess Returns...")
    excess_returns = shv_returns - daily_rf_rates
    
    print(f"Average Excess Return (Daily): {excess_returns.mean()*100:.5f}%")
    print(f"Excess Return Std Dev (Daily): {excess_returns.std()*100:.5f}%")
    
    # 4. Calculate Sharpe components
    print("\n4. Sharpe Ratio Components...")
    annualized_excess_return = excess_returns.mean() * TRADING_DAYS_YEAR * 100
    annualized_vol = excess_returns.std() * np.sqrt(TRADING_DAYS_YEAR) * 100
    sharpe = np.sqrt(TRADING_DAYS_YEAR) * (excess_returns.mean() / excess_returns.std())
    
    print(f"Annualized Excess Return: {annualized_excess_return:.2f}%")
    print(f"Annualized Volatility: {annualized_vol:.2f}%")
    print(f"Final Sharpe Ratio: {sharpe:.2f}")
    
    # 5. Additional Analysis
    print("\n5. Return Distribution Analysis...")
    print(f"Return Skewness: {shv_returns.skew():.2f}")
    print(f"Return Kurtosis: {shv_returns.kurtosis():.2f}")
    print(f"Percent Positive Returns: {(shv_returns > 0).mean()*100:.1f}%")
    print(f"Percent Above Risk-Free: {(excess_returns > 0).mean()*100:.1f}%")
    
    # 6. Sample of recent calculations
    print("\n6. Last 5 Days Detail:")
    recent_data = pd.DataFrame({
        'SHV Return': shv_returns.tail() * 100,
        'Daily RF Rate': daily_rf_rates.tail() * 100,
        'Excess Return': excess_returns.tail() * 100
    })
    print(recent_data.round(5))

if __name__ == "__main__":
    analyze_shv_sharpe()
