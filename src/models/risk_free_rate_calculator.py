"""
Risk Free Rate Calculator
Uses BIL ETF to calculate risk-free rate based on dividend yield
"""
import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def calculate_bil_risk_free_rate():
    """
    Calculate risk-free rate using BIL ETF's 2-year dividend yield
    Returns:
        tuple: (risk_free_rate, avg_price, total_dividends)
    """
    try:
        # Fetch BIL data
        bil = yf.Ticker("BIL")
        
        # Get 2 years of price history using period
        price_history = bil.history(period="2y")
        avg_price = price_history['Close'].mean()
        
        # Get dividend history for same period
        dividends = bil.dividends
        recent_dividends = dividends[-504:]  # Last 2 years of trading days
        total_dividends = recent_dividends.sum()
        
        # Calculate annualized yield
        risk_free_rate = (total_dividends / 2) / avg_price
        
        return risk_free_rate, avg_price, total_dividends
        
    except Exception as e:
        logger.error(f"Error calculating BIL risk-free rate: {str(e)}")
        return None, None, None

def calculate_shv_yield():
    """Calculate SHV yield for comparison"""
    try:
        shv = yf.Ticker("SHV")
        
        # Get 2 years of price history
        price_history = shv.history(period="2y")
        avg_price = price_history['Close'].mean()
        
        # Get dividend history
        dividends = shv.dividends
        recent_dividends = dividends[-504:]  # Last 2 years of trading days
        total_dividends = recent_dividends.sum()
        
        risk_free_rate = (total_dividends / 2) / avg_price
        
        return risk_free_rate, avg_price, total_dividends
        
    except Exception as e:
        logger.error(f"Error calculating SHV yield: {str(e)}")
        return None, None, None

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Calculate BIL rate
    logger.info("\nCalculating BIL risk-free rate...")
    bil_rate, bil_price, bil_divs = calculate_bil_risk_free_rate()
    
    if bil_rate is not None:
        logger.info(f"BIL 2-year average price: ${bil_price:.2f}")
        logger.info(f"BIL 2-year total dividends: ${bil_divs:.4f}")
        logger.info(f"BIL implied risk-free rate: {bil_rate*100:.2f}%")
    
    # Calculate SHV for comparison
    logger.info("\nCalculating SHV yield for comparison...")
    shv_rate, shv_price, shv_divs = calculate_shv_yield()
    
    if shv_rate is not None:
        logger.info(f"SHV 2-year average price: ${shv_price:.2f}")
        logger.info(f"SHV 2-year total dividends: ${shv_divs:.4f}")
        logger.info(f"SHV implied yield: {shv_rate*100:.2f}%")
