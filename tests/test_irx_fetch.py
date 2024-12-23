import sys
import os
import logging
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_irx_fetch():
    try:
        # Test weekly data fetch
        logger.info("\nTesting weekly ^IRX fetch...")
        irx = yf.Ticker("^IRX")
        
        # Try max period first
        logger.info("Fetching maximum available weekly data...")
        weekly_data = irx.history(period='max', interval='1wk')
        
        if weekly_data.empty:
            logger.error("Weekly ^IRX data fetch returned empty dataset")
            return
            
        logger.info(f"Successfully fetched {len(weekly_data)} weeks of ^IRX data")
        logger.info(f"Weekly data range: {weekly_data.index[0]} to {weekly_data.index[-1]}")
        logger.info(f"Sample of rates:")
        logger.info(weekly_data['Close'].tail().to_string())
        
        # Also try 5y period for comparison
        logger.info("\nFetching 5 years of weekly data...")
        weekly_data_5y = irx.history(period='5y', interval='1wk')
        logger.info(f"5y weekly data: {len(weekly_data_5y)} weeks")
        logger.info(f"5y range: {weekly_data_5y.index[0]} to {weekly_data_5y.index[-1]}")
            
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        logger.error(f"Exception type: {type(e).__name__}")

if __name__ == "__main__":
    test_irx_fetch()
