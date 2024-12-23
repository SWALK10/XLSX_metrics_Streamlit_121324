"""
Test version of metrics calculator with NA handling
"""
import pandas as pd
import numpy as np
from typing import Dict

class MetricsCalculatorTest:
    """Simplified metrics calculator that handles NA values"""
    
    def __init__(self):
        self.min_history_days = 504  # 2 years for Sharpe
        
    def calculate_metrics(self, prices: pd.Series) -> Dict:
        """
        Calculate metrics handling NA values
        Returns empty values if insufficient data
        """
        metrics = {}
        
        # Remove NA values for calculations
        clean_prices = prices.dropna()
        
        # Basic return calculations
        try:
            # Daily return (most recent)
            if len(clean_prices) >= 2:
                daily_return = (clean_prices.iloc[-1] / clean_prices.iloc[-2] - 1)
                metrics['Day%'] = daily_return
            else:
                metrics['Day%'] = np.nan
                
            # One month return (21 trading days)
            if len(clean_prices) >= 21:
                month_return = (clean_prices.iloc[-1] / clean_prices.iloc[-21] - 1)
                metrics['1MTH%'] = month_return
            else:
                metrics['1MTH%'] = np.nan
                
            # YTD return
            year_start = pd.Timestamp(pd.Timestamp.now().year, 1, 1)
            ytd_prices = clean_prices[clean_prices.index >= year_start]
            if not ytd_prices.empty:
                ytd_return = (ytd_prices.iloc[-1] / ytd_prices.iloc[0] - 1)
                metrics['YTD%'] = ytd_return
            else:
                metrics['YTD%'] = np.nan
                
            # Sharpe ratio (only if we have 2 years of data)
            if len(clean_prices) >= self.min_history_days:
                returns = clean_prices.pct_change().dropna()
                excess_returns = returns - 0.03/252  # Simple 3% risk-free rate
                sharpe = np.sqrt(252) * (excess_returns.mean() / returns.std())
                metrics['Sharpe 2Y'] = sharpe
            else:
                metrics['Sharpe 2Y'] = np.nan
                
        except Exception as e:
            print(f"Error calculating metrics: {str(e)}")
            # Fill any missing metrics with NA
            for key in ['Day%', '1MTH%', 'YTD%', 'Sharpe 2Y']:
                if key not in metrics:
                    metrics[key] = np.nan
        
        return metrics

def calculate_all_ticker_metrics(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate metrics for all tickers in the DataFrame
    Returns DataFrame with metrics for each ticker
    """
    calc = MetricsCalculatorTest()
    all_metrics = []
    
    for ticker in price_df.columns:
        metrics = calc.calculate_metrics(price_df[ticker])
        metrics['Ticker'] = ticker
        all_metrics.append(metrics)
    
    # Convert to DataFrame
    metrics_df = pd.DataFrame(all_metrics)
    
    # Reorder columns
    col_order = ['Ticker', 'Day%', '1MTH%', 'YTD%', 'Sharpe 2Y']
    metrics_df = metrics_df[col_order]
    
    return metrics_df
