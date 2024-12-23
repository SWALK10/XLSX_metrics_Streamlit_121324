"""
Test version of Excel Manager focused on Sharpe ratio calculations
Maintains core functionality while adding test capabilities
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime, date
import yfinance as yf
import logging
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestSharpeManager:
    """
    Test implementation for Sharpe ratio calculations
    Focuses on dividend-adjusted data and BIL comparison
    """
    
    REQUEST_DELAY = 4
    MAX_RETRIES = 3
    
    def __init__(self):
        """Initialize the test manager"""
        logger.info("Test Sharpe Manager initialized")
    
    def get_risk_free_rate(self, start_date: date, end_date: date) -> float:
        """Get risk-free rate from BIL ETF"""
        try:
            bil = yf.download('BIL', start=start_date, end=end_date)
            if not bil.empty:
                # Calculate annualized return
                daily_rf = bil['Adj Close'].pct_change().mean()
                annual_rf = (1 + daily_rf) ** 252 - 1
                return annual_rf
            return 0.03  # Default 3% if BIL data unavailable
        except Exception as e:
            logger.warning(f"Error getting risk-free rate: {e}")
            return 0.03

    def calculate_sharpe_ratio(self, prices: pd.Series, 
                             start_date: Optional[date] = None,
                             end_date: Optional[date] = None) -> Tuple[float, float]:
        """
        Calculate both current and standard Sharpe ratio implementations
        
        Args:
            prices: Series of dividend-adjusted prices
            start_date: Optional start date for calculation
            end_date: Optional end date for calculation
            
        Returns:
            Tuple of (current_implementation, standard_implementation)
        """
        if start_date is None:
            start_date = prices.index[0]
        if end_date is None:
            end_date = prices.index[-1]
            
        # Get data for date range
        mask = (prices.index >= start_date) & (prices.index <= end_date)
        prices = prices[mask]
        
        # Calculate daily returns
        daily_returns = prices.pct_change().dropna()
        
        # Get risk-free rate
        rf_rate = self.get_risk_free_rate(start_date, end_date)
        daily_rf = (1 + rf_rate) ** (1/252) - 1
        
        # Current implementation (using daily returns std)
        annual_return = (1 + daily_returns.mean()) ** 252 - 1
        annual_std = daily_returns.std() * np.sqrt(252)
        current_sharpe = (annual_return - rf_rate) / annual_std if annual_std != 0 else 0
        
        # Standard implementation (using excess returns std)
        excess_returns = daily_returns - daily_rf
        annual_excess_return = (1 + excess_returns.mean()) ** 252 - 1
        annual_excess_std = excess_returns.std() * np.sqrt(252)
        standard_sharpe = annual_excess_return / annual_excess_std if annual_excess_std != 0 else 0
        
        return current_sharpe, standard_sharpe

    def get_test_data(self, ticker: str, 
                      start_date: str = '2020-01-01',
                      end_date: Optional[str] = None) -> pd.Series:
        """Get dividend-adjusted test data for a ticker"""
        if end_date is None:
            end_date = date.today().strftime('%Y-%m-%d')
            
        try:
            data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
            return data['Close']
        except Exception as e:
            logger.error(f"Error getting test data for {ticker}: {e}")
            return pd.Series()
