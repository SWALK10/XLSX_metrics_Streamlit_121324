"""
ETF Data Manager
Handles ETF-specific data operations and validations.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import logging
from typing import Dict, List, Optional, Tuple, Any
import time

logger = logging.getLogger(__name__)

class ETFManager:
    """Manages ETF-specific data operations"""
    
    # Constants for ETF validation
    MIN_ASSETS = 1_000_000  # Minimum assets under management
    MIN_VOLUME = 10_000     # Minimum daily trading volume
    MAX_EXPENSE = 2.0       # Maximum expense ratio (%)
    
    def __init__(self):
        """Initialize ETF Manager"""
        self.cache = {}
        self.last_request = datetime.now()
        self.REQUEST_DELAY = 2  # seconds between requests
        
    def validate_etf(self, ticker: str) -> Tuple[bool, str]:
        """
        Validate if a ticker is a valid ETF meeting criteria
        Args:
            ticker: ETF ticker symbol
        Returns:
            (is_valid, message) tuple
        """
        try:
            info = self._get_etf_info(ticker)
            if info is None:
                return False, "Failed to fetch ETF info"
                
            # Check if it's actually an ETF
            if info.get('quoteType', '').lower() != 'etf':
                return False, f"{ticker} is not an ETF"
                
            # Validate AUM
            total_assets = info.get('totalAssets', 0)
            if total_assets < self.MIN_ASSETS:
                return False, f"AUM too low: ${total_assets:,.0f}"
                
            # Validate volume
            avg_volume = info.get('averageVolume', 0)
            if avg_volume < self.MIN_VOLUME:
                return False, f"Volume too low: {avg_volume:,.0f}"
                
            # Validate expense ratio
            expense_ratio = info.get('expenseRatio', 0) * 100 if 'expenseRatio' in info else None
            if expense_ratio and expense_ratio > self.MAX_EXPENSE:
                return False, f"Expense ratio too high: {expense_ratio:.2f}%"
                
            return True, "Valid ETF"
            
        except Exception as e:
            logger.error(f"Error validating ETF {ticker}: {str(e)}")
            return False, f"Validation error: {str(e)}"
            
    def _get_etf_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get ETF information
        Args:
            ticker: ETF ticker symbol
        Returns:
            Dictionary with ETF info or None if failed
        """
        try:
            # Rate limiting
            now = datetime.now()
            time_since_last = (now - self.last_request).total_seconds()
            if time_since_last < self.REQUEST_DELAY:
                time.sleep(self.REQUEST_DELAY - time_since_last)
                
            etf = yf.Ticker(ticker)
            info = etf.info
            self.last_request = datetime.now()
            return info
            
        except Exception as e:
            logger.error(f"Error fetching ETF info for {ticker}: {str(e)}")
            return None
            
    def get_holdings(self, ticker: str) -> Optional[pd.DataFrame]:
        """
        Get ETF holdings if available
        Args:
            ticker: ETF ticker symbol
        Returns:
            DataFrame with holdings or None if unavailable
        """
        try:
            etf = yf.Ticker(ticker)
            holdings = etf.holdings
            if holdings is None or holdings.empty:
                logger.warning(f"No holdings data available for {ticker}")
                return None
            return holdings
            
        except Exception as e:
            logger.error(f"Error fetching holdings for {ticker}: {str(e)}")
            return None
            
    def get_sector_weights(self, ticker: str) -> Optional[Dict[str, float]]:
        """
        Get ETF sector weights if available
        Args:
            ticker: ETF ticker symbol
        Returns:
            Dictionary of sector weights or None if unavailable
        """
        try:
            etf = yf.Ticker(ticker)
            sector_info = etf.sector
            if not sector_info:
                logger.warning(f"No sector data available for {ticker}")
                return None
            return sector_info
            
        except Exception as e:
            logger.error(f"Error fetching sector weights for {ticker}: {str(e)}")
            return None
            
    def calculate_metrics(self, ticker: str) -> Dict[str, Any]:
        """
        Calculate ETF-specific metrics
        Args:
            ticker: ETF ticker symbol
        Returns:
            Dictionary of metrics
        """
        metrics = {}
        try:
            info = self._get_etf_info(ticker)
            if info:
                # Basic info
                metrics['name'] = info.get('longName', 'N/A')
                metrics['category'] = info.get('category', 'N/A')
                metrics['aum'] = info.get('totalAssets', 0)
                metrics['expense_ratio'] = info.get('expenseRatio', 0) * 100 if 'expenseRatio' in info else None
                
                # Trading metrics
                metrics['avg_volume'] = info.get('averageVolume', 0)
                metrics['ytd_return'] = info.get('ytdReturn', None)
                
                # Risk metrics
                metrics['beta'] = info.get('beta', None)
                metrics['tracking_error'] = info.get('trackingError', None)
                
            # Get holdings concentration
            holdings = self.get_holdings(ticker)
            if holdings is not None:
                metrics['num_holdings'] = len(holdings)
                metrics['top_10_weight'] = holdings['Weight'].nlargest(10).sum()
                
            # Get sector diversification
            sectors = self.get_sector_weights(ticker)
            if sectors:
                metrics['num_sectors'] = len(sectors)
                metrics['top_sector'] = max(sectors.items(), key=lambda x: x[1])[0]
                metrics['top_sector_weight'] = max(sectors.values())
                
        except Exception as e:
            logger.error(f"Error calculating metrics for {ticker}: {str(e)}")
            
        return metrics
