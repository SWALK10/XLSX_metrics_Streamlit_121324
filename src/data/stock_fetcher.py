"""
Stock Data Fetcher
Handles downloading and caching of stock data from yfinance.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import logging
import time
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class StockFetcher:
    """Handles downloading and caching of stock data"""
    
    def __init__(self):
        """Initialize the stock fetcher"""
        self.cache = {}
        self.last_request = datetime.now()
        self.REQUEST_DELAY = 2  # seconds between requests
        
    def get_stock_data(self, ticker: str, period: str = "5y") -> Optional[pd.DataFrame]:
        """
        Get stock data for a ticker
        Args:
            ticker: Stock ticker symbol
            period: Data period (default: 5y)
        Returns:
            DataFrame with stock data or None if failed
        """
        try:
            # Rate limiting
            now = datetime.now()
            time_since_last = (now - self.last_request).total_seconds()
            if time_since_last < self.REQUEST_DELAY:
                time.sleep(self.REQUEST_DELAY - time_since_last)
            
            # Download data
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                logger.warning(f"No data found for {ticker}")
                return None
                
            # Cache the result
            self.cache[ticker] = hist
            self.last_request = datetime.now()
            
            return hist
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return None
            
    def get_stock_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get stock information
        Args:
            ticker: Stock ticker symbol
        Returns:
            Dictionary with stock info or None if failed
        """
        try:
            stock = yf.Ticker(ticker)
            return stock.info
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {str(e)}")
            return None
