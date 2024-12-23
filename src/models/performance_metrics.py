"""
Performance Metrics Calculator
Handles all performance and risk metric calculations.
"""
import pandas as pd
import numpy as np
import logging
from typing import Dict, Optional, Union, List, Tuple
import yfinance as yf

logger = logging.getLogger(__name__)

def calculate_bil_risk_free_rate() -> float:
    """
    Calculate risk-free rate using BIL ETF's 2-year dividend yield
    Returns:
        float: Annualized risk-free rate
    """
    try:
        print("DEBUG: Starting BIL risk-free rate calculation")
        # Fetch BIL data
        bil = yf.Ticker("BIL")
        
        # Get 2 years of price history
        price_history = bil.history(period="2y")
        avg_price = price_history['Close'].mean()
        print(f"DEBUG: BIL average price: {avg_price}")
        
        # Get dividend history
        dividends = bil.dividends
        recent_dividends = dividends[-504:]  # Last 2 years of trading days
        total_dividends = recent_dividends.sum()
        print(f"DEBUG: BIL total dividends: {total_dividends}")
        
        # Calculate annualized yield
        risk_free_rate = (total_dividends / 2) / avg_price
        print(f"DEBUG: Calculated risk-free rate: {risk_free_rate}")
        
        return risk_free_rate
        
    except Exception as e:
        print(f"DEBUG: Error calculating BIL risk-free rate: {str(e)}")
        return 0.03  # Default to 3% if calculation fails

class PerformanceMetrics:
    """Calculates performance and risk metrics for stocks"""
    
    # Constants for calculations
    TRADING_DAYS_YEAR = 252
    MIN_HISTORY_DAYS = 504  # 2 years minimum for Sharpe ratio
    
    def __init__(self):
        """Initialize Performance Metrics calculator"""
        self._risk_free_rate = None
        self._last_rate_fetch = None
    
    def _get_risk_free_rate(self) -> float:
        """
        Get current risk-free rate using BIL ETF
        Returns:
            float: Annualized risk-free rate
        """
        return calculate_bil_risk_free_rate()
    
    def calculate_returns(self, prices: pd.Series) -> Dict[str, float]:
        """
        Calculate various return metrics
        Args:
            prices: Series of daily adjusted closing prices
        Returns:
            Dictionary of return metrics
        """
        try:
            returns = {}
            
            # Daily return
            returns['daily_return'] = self._calculate_return(prices, 1)
            
            # Weekly return (5 trading days)
            returns['weekly_return'] = self._calculate_return(prices, 5)
            
            # Monthly return (21 trading days)
            returns['one_month_return'] = self._calculate_return(prices, 21)
            
            # YTD return
            returns['ytd_return'] = self._calculate_ytd_return(prices)
            
            # 1-year return
            returns['one_year_return'] = self._calculate_return(prices, self.TRADING_DAYS_YEAR)
            
            # Annualized return
            returns['annualized_return'] = self._calculate_annualized_return(prices)
            
            return returns
            
        except Exception as e:
            logger.error(f"Error calculating returns: {str(e)}")
            return {}
            
    def calculate_risk_metrics(self, prices: pd.Series) -> Dict[str, Union[float, Tuple[float, bool]]]:
        """
        Calculate risk metrics including Sharpe ratio
        Args:
            prices: Series of daily adjusted closing prices
        Returns:
            Dictionary of risk metrics
        """
        try:
            metrics = {}
            
            # Ensure we have enough data
            if len(prices) < self.MIN_HISTORY_DAYS:
                logger.warning(f"Insufficient data for risk metrics. Need {self.MIN_HISTORY_DAYS} days, got {len(prices)}")
                return metrics
            
            # Get exactly 504 trading days of data, starting from most recent
            prices = prices.sort_index()[-self.MIN_HISTORY_DAYS:]
            
            # Calculate daily returns for volatility
            daily_returns = prices.pct_change().dropna()
            
            # Get risk-free rate
            annual_rf_rate = self._get_risk_free_rate()
            
            # Convert annual risk-free rate to daily
            daily_rf_rate = annual_rf_rate / self.TRADING_DAYS_YEAR
            
            # Calculate excess returns (use daily rates)
            excess_returns = daily_returns - daily_rf_rate
            
            # Daily Sharpe ratio (use returns std, not excess returns std)
            daily_sharpe = excess_returns.mean() / daily_returns.std()
            
            # Annualize Sharpe ratio
            sharpe = daily_sharpe * np.sqrt(self.TRADING_DAYS_YEAR)
            
            # Store Sharpe ratio and risk-free rate
            metrics['sharpe_2y'] = sharpe
            metrics['annual_rf_rate'] = annual_rf_rate
            
            # Volatility (annualized)
            daily_vol = daily_returns.std()
            metrics['volatility'] = daily_vol * np.sqrt(self.TRADING_DAYS_YEAR)
            
            # Maximum drawdown
            metrics['max_drawdown'] = self._calculate_max_drawdown(prices)
            
            # Value at Risk (95%)
            metrics['var_95'] = self._calculate_var(daily_returns, 0.95)
            
            # Sortino ratio
            metrics['sortino_ratio'] = self._calculate_sortino_ratio(daily_returns)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics: {str(e)}")
            return {}
            
    def _calculate_return(self, prices: pd.Series, periods: int) -> Optional[float]:
        """Calculate return over specified number of periods"""
        try:
            if len(prices) < periods + 1:
                return None
            return (prices.iloc[-1] / prices.iloc[-periods-1]) - 1
        except Exception:
            return None
            
    def _calculate_ytd_return(self, prices: pd.Series) -> Optional[float]:
        """Calculate year-to-date return"""
        try:
            current_year = pd.Timestamp('today').year
            ytd_prices = prices[prices.index.year >= current_year]
            if len(ytd_prices) < 2:
                return None
            return (ytd_prices.iloc[-1] / ytd_prices.iloc[0]) - 1
        except Exception:
            return None
            
    def _calculate_annualized_return(self, prices: pd.Series) -> Optional[float]:
        """Calculate annualized return"""
        try:
            if len(prices) < 2:
                return None
            days = (prices.index[-1] - prices.index[0]).days
            if days < 1:
                return None
            total_return = (prices.iloc[-1] / prices.iloc[0]) - 1
            return (1 + total_return) ** (365.25 / days) - 1
        except Exception:
            return None
            
    def _calculate_max_drawdown(self, prices: pd.Series) -> Optional[float]:
        """Calculate maximum drawdown"""
        try:
            peak = prices.expanding(min_periods=1).max()
            drawdown = (prices - peak) / peak
            return drawdown.min()
        except Exception:
            return None
            
    def calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rates: pd.Series) -> float:
        """
        Calculate Sharpe ratio using historical risk-free rates.
        
        Args:
            returns (pd.Series): Daily returns
            risk_free_rates (pd.Series): Daily risk-free rates (annual rates / 252)
        
        Returns:
            float: Annualized Sharpe ratio, rounded to 2 decimal places
        
        Notes:
            - Uses historical Treasury rates (^IRX) instead of fixed rate
            - Aligns rates with return dates
            - Returns are annualized using √252
        """
        try:
            # Input validation
            if returns is None or risk_free_rates is None:
                return 0.0
            
            if len(returns) < 2:
                return 0.0
            
            # Calculate excess returns using daily rates
            daily_rf_rate = risk_free_rates / 252  # Convert annual to daily
            excess_returns = returns - daily_rf_rate
            
            # WORKING ONLY - Change with Permission
            # Critical calculation: Calculate Sharpe using daily rates, then annualize
            # DO NOT modify this calculation without explicit permission - last verified 2024-12-15
            # Calculate daily metrics first
            daily_excess_return = excess_returns.mean()
            daily_volatility = excess_returns.std()
            
            # Annualize the ratio, not the components
            sharpe = (daily_excess_return / daily_volatility) * np.sqrt(252)
            
            # Round to 2 decimal places for consistency
            return round(sharpe, 2)
        
        except Exception as e:
            logger.error(f"Error in Sharpe calculation: {str(e)}")
            return 0.0
            
    def _calculate_var(self, returns: pd.Series, confidence: float) -> Optional[float]:
        """Calculate Value at Risk"""
        try:
            return np.percentile(returns, (1 - confidence) * 100)
        except Exception:
            return None
            
    def _calculate_sortino_ratio(self, returns: pd.Series) -> Optional[float]:
        """Calculate Sortino ratio"""
        try:
            # Get aligned treasury rates for consistency with Sharpe
            annual_rf_rate = self._get_risk_free_rate()
            daily_rf_rates = annual_rf_rate / self.TRADING_DAYS_YEAR
            
            excess_returns = returns - daily_rf_rates
            downside_returns = excess_returns[excess_returns < 0]
            if len(downside_returns) == 0:
                return None
            downside_std = np.sqrt(np.mean(downside_returns**2))
            if downside_std == 0:
                return None
            return np.sqrt(self.TRADING_DAYS_YEAR) * (excess_returns.mean() / downside_std)
        except Exception as e:
            logger.error(f"Error calculating Sortino ratio: {str(e)}")
            return None
            
    def calculate_all_metrics(self, prices: pd.Series) -> Dict[str, float]:
        """
        Calculate all performance and risk metrics
        Args:
            prices: Series of daily adjusted closing prices
        Returns:
            Dictionary of all metrics
        """
        print("DEBUG: Starting calculate_all_metrics")
        metrics = {}
        
        # Get return metrics
        returns = self.calculate_returns(prices)
        print(f"DEBUG: Return metrics: {returns}")
        metrics.update(returns)
        
        # Get risk metrics
        risk_metrics = self.calculate_risk_metrics(prices)
        print(f"DEBUG: Risk metrics: {risk_metrics}")
        metrics.update(risk_metrics)
        
        print(f"DEBUG: Final metrics: {metrics}")
        return metrics
