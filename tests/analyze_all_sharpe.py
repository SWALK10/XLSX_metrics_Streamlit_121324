"""
Compare Sharpe ratios for all ETFs with XLSX values
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_sharpe(ticker):
    # Constants
    TRADING_DAYS_YEAR = 252
    
    # Get ETF data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2*365)
    
    etf = yf.Ticker(ticker)
    etf_data = etf.history(start=start_date)
    returns = etf_data['Close'].pct_change().dropna()
    
    # Get Treasury rates
    irx = yf.Ticker("^IRX")
    irx_data = irx.history(start=start_date - timedelta(days=30))
    treasury_rates = irx_data['Close'] / 100
    treasury_rates = treasury_rates.ffill().bfill()
    
    # Align rates with returns
    aligned_rates = treasury_rates.reindex(returns.index, method='ffill')
    daily_rf_rates = aligned_rates / TRADING_DAYS_YEAR
    
    # Calculate excess returns
    excess_returns = returns - daily_rf_rates
    
    # Calculate Sharpe
    sharpe = np.sqrt(TRADING_DAYS_YEAR) * (excess_returns.mean() / excess_returns.std())
    
    # Additional stats for analysis
    stats = {
        'ticker': ticker,
        'avg_return': returns.mean() * 100,
        'volatility': returns.std() * np.sqrt(TRADING_DAYS_YEAR) * 100,
        'sharpe': round(sharpe, 2),
        'rf_rate': aligned_rates.mean() * 100,
        'excess_return': excess_returns.mean() * TRADING_DAYS_YEAR * 100
    }
    return stats

def main():
    # ETFs from dashboard
    etfs = ['TLT', 'SPY', 'JNK', 'HYG', 'BKLN', 'SJNK', 'SHV']
    
    # XLSX Sharpe values
    xlsx_sharpe = {
        'TLT': -0.41,
        'SPY': 0.63,
        'JNK': 0.05,
        'HYG': 0.07,
        'BKLN': 0.18,
        'SJNK': 0.26,
        'SHV': -2.32
    }
    
    print("\nComparing Sharpe Ratios: Calculated vs XLSX")
    print("-" * 60)
    print(f"{'ETF':6} {'Calc Sharpe':>12} {'XLSX Sharpe':>12} {'Diff':>8} {'Avg Ret%':>10} {'Vol%':>8} {'RF%':>6}")
    print("-" * 60)
    
    for etf in etfs:
        stats = calculate_sharpe(etf)
        diff = stats['sharpe'] - xlsx_sharpe[etf]
        print(f"{etf:6} {stats['sharpe']:12.2f} {xlsx_sharpe[etf]:12.2f} {diff:8.2f} "
              f"{stats['avg_return']:10.2f} {stats['volatility']:8.1f} {stats['rf_rate']:6.1f}")
        
        if abs(diff) > 0.5:  # Highlight significant differences
            print(f"Detailed analysis for {etf}:")
            print(f"  Annualized Excess Return: {stats['excess_return']:.2f}%")
            print(f"  Daily Sharpe Components:")
            print(f"    - Average Return: {stats['avg_return']/252:.5f}%")
            print(f"    - Average RF Rate: {stats['rf_rate']/252:.5f}%")
            print(f"    - Daily Volatility: {stats['volatility']/np.sqrt(252):.5f}%")
            print()

if __name__ == "__main__":
    main()
