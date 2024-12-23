"""
Treasury Rate Manager
Handles fetching and caching of Treasury rates for risk-free rate calculations
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class TreasuryRateManager:
    """Manages Treasury rate data for risk-free rate calculations"""
    
    def __init__(self, cache_dir: str = None):
        """
        Initialize Treasury Rate Manager
        Args:
            cache_dir: Directory to store cached rates. If None, uses default
        """
        if cache_dir is None:
            cache_dir = Path("data/treasury_rates")
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / "treasury_rates.parquet"
        self.ticker = "^IRX"  # 13-week Treasury Bill
        self._ensure_cache_dir()
        
    def _ensure_cache_dir(self):
        """Ensure cache directory exists"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_cached_rates(self) -> pd.DataFrame:
        """Load cached rates from parquet file"""
        if self.cache_file.exists():
            try:
                return pd.read_parquet(self.cache_file)
            except Exception as e:
                logger.error(f"Error loading cached rates: {e}")
        return pd.DataFrame()
        
    def _save_rates_cache(self, rates: pd.DataFrame):
        """Save rates to cache file"""
        try:
            rates.to_parquet(self.cache_file)
        except Exception as e:
            logger.error(f"Error saving rates cache: {e}")
            
    def get_treasury_rates(self, start_date: datetime, end_date: datetime) -> pd.Series:
        """
        Get Treasury rates for date range, using cache when possible
        Args:
            start_date: Start date for rates
            end_date: End date for rates
        Returns:
            Series of daily Treasury rates (as decimals)
        """
        # Load cached data
        cached_rates = self._load_cached_rates()
        
        # Convert dates to pandas datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Initialize result series
        result = pd.Series(dtype=float)
        
        # If we have cached data, use it
        if not cached_rates.empty:
            cached_rates.index = pd.to_datetime(cached_rates.index)
            result = cached_rates[start_date:end_date]
        
        # If we're missing any dates, fetch from yfinance
        if result.empty or (end_date - result.index[-1]).days > 1:
            fetch_start = start_date
            if not result.empty:
                fetch_start = result.index[-1] + timedelta(days=1)
                
            try:
                treasury = yf.Ticker(self.ticker)
                new_rates = treasury.history(start=fetch_start, end=end_date + timedelta(days=1))
                if not new_rates.empty:
                    # Convert percentage to decimal
                    new_rates = new_rates['Close'] / 100.0
                    
                    # Combine with cached data
                    if result.empty:
                        result = new_rates
                    else:
                        result = pd.concat([result, new_rates])
                    
                    # Update cache with all data
                    self._save_rates_cache(result)
            except Exception as e:
                logger.error(f"Error fetching Treasury rates: {e}")
        
        return result
        
    def get_current_rate(self) -> float:
        """
        Get most recent Treasury rate
        Returns:
            Latest Treasury rate as decimal (e.g., 0.0422 for 4.22%)
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)  # Get last 5 days in case of holidays
        
        rates = self.get_treasury_rates(start_date, end_date)
        if not rates.empty:
            return rates.iloc[-1]
        return 0.03  # Fallback to 3% if unable to get rate
