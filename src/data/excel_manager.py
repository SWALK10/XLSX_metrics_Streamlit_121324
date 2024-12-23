"""
Excel Data Manager for Stock Dashboard
Handles all Excel-based data storage and retrieval operations.
Uses daily data only, no intraday prices.

Usage Parameters:
- Typical Usage: 1-20 tickers per analysis
- Frequency: 3-10 analyses per day
- Data Type: End-of-day prices only
- Output: View-only Excel files
- No manual modifications to generated files

Memory Management:
- Efficient for up to 20 tickers
- Clears DataFrame memory after each analysis
- Implements file size monitoring
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import yfinance as yf
import logging
from typing import Dict, List, Optional, Tuple
import time
from ..models.metrics_writer import calculate_and_write_metrics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExcelManager:
    """
    Manages Excel-based data storage and retrieval.
    All price data is daily close prices only.
    """
    
    # Excel sheet names
    DAILY_PRICES_SHEET = 'Daily Prices'
    UNADJUSTED_PRICES_SHEET = 'Unadjusted Prices'
    DIVIDENDS_SHEET = 'Dividends'
    CALCULATIONS_SHEET = 'Metrics'
    
    # Rate limiting parameters
    REQUEST_DELAY = 4  # seconds between requests
    MAX_RETRIES = 3
    MAX_FILENAME_TICKERS = 3  # Maximum number of tickers to include in filename
    
    def __init__(self, data_dir: str, tickers: List[str] = None):
        """
        Initialize the Excel Manager
        Args:
            data_dir: Base directory for Excel files
            tickers: List of tickers being processed
        """
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Generate dated Excel file path with timestamp and first 3 tickers
        now = datetime.now()
        date_str = now.strftime('%Y%m%d_%H%M')
        ticker_str = ''
        if tickers:
            display_tickers = tickers[:self.MAX_FILENAME_TICKERS]
            ticker_str = '_' + '_'.join(display_tickers)
            if len(tickers) > self.MAX_FILENAME_TICKERS:
                logger.info(f"Using first {self.MAX_FILENAME_TICKERS} tickers in filename out of {len(tickers)} total tickers")
        
        self.excel_path = os.path.join(self.data_dir, f"dashboard_data_{date_str}{ticker_str}.xlsx")
        self.ensure_excel_file()
        logger.info(f"Excel Manager initialized with data directory: {self.data_dir}")

    def ensure_excel_file(self):
        """Create Excel file with required sheets if it doesn't exist"""
        if not os.path.exists(self.excel_path):
            logger.info(f"Creating new Excel file at {self.excel_path}")
            try:
                with pd.ExcelWriter(self.excel_path, engine='xlsxwriter') as writer:
                    # Create empty DataFrames with datetime index
                    empty_df = pd.DataFrame(index=pd.date_range(start='2020-01-01', periods=1))
                    empty_df.index.name = 'Date'
                    
                    # Save empty sheets
                    empty_df.to_excel(writer, sheet_name=self.DAILY_PRICES_SHEET)
                    empty_df.to_excel(writer, sheet_name=self.UNADJUSTED_PRICES_SHEET)
                    empty_df.to_excel(writer, sheet_name=self.DIVIDENDS_SHEET)
                    # Metrics sheet will be created when we have data to write
                logger.info("Successfully created Excel file")
            except PermissionError:
                logger.error(f"Permission denied: Could not create {self.excel_path}. Please close the file if it's open.")
                raise
            except Exception as e:
                logger.error(f"Failed to create Excel file: {str(e)}")
                raise

    def download_ticker_data(self, ticker: str) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """
        Download price and dividend data for a ticker starting from 2020-01-01
        Returns: (adjusted_prices, unadjusted_prices, dividends)
        """
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                # Set date range
                start_date = '2020-01-01'
                end_date = date.today().strftime('%Y-%m-%d')
                logger.info(f"Fetching data for {ticker} from {start_date} to {end_date}")
                
                # Download data
                stock = yf.Ticker(ticker)
                
                # Get adjusted price data
                logger.info(f"Getting adjusted price history for {ticker}")
                adj_hist = stock.history(start=start_date, end=end_date, auto_adjust=True)
                if adj_hist.empty:
                    logger.warning(f"No data found for {ticker} on attempt {retries + 1}")
                    retries += 1
                    continue
                
                # Get unadjusted price data
                logger.info(f"Getting unadjusted price history for {ticker}")
                unadj_hist = stock.history(start=start_date, end=end_date, auto_adjust=False)
                
                # Get comprehensive dividend data
                try:
                    logger.info(f"Getting dividend history for {ticker}")
                    # Get both actions and dividends to ensure we don't miss any
                    actions_div = stock.actions[['Dividends']].loc[start_date:end_date]
                    regular_div = stock.dividends.loc[start_date:end_date].to_frame()
                    
                    # Combine both sources and remove duplicates
                    if not actions_div.empty:
                        actions_div.columns = [ticker]  # Use ticker as column name
                    if not regular_div.empty:
                        regular_div.columns = [ticker]  # Use ticker as column name
                    
                    dividends = pd.concat([actions_div, regular_div]).sort_index()
                    dividends = dividends[~dividends.index.duplicated(keep='first')]  # Remove duplicates
                    dividends = dividends[dividends[ticker] > 0]  # Filter out zero dividends
                    
                    logger.info(f"Found {len(dividends)} dividend records")
                except Exception as div_err:
                    logger.warning(f"Error fetching dividends for {ticker}: {str(div_err)}")
                    dividends = pd.DataFrame(columns=[ticker])
                
                # Convert timezone-aware dates to dates only
                adj_hist.index = adj_hist.index.date
                unadj_hist.index = unadj_hist.index.date
                if not dividends.empty:
                    dividends.index = dividends.index.date
                
                # Create single-column dataframes with ticker as column name
                adj_prices = pd.DataFrame({ticker: adj_hist['Close']})
                unadj_prices = pd.DataFrame({ticker: unadj_hist['Close']})
                
                logger.info(f"Successfully downloaded data for {ticker}")
                return adj_prices, unadj_prices, dividends
                
            except Exception as e:
                logger.error(f"Error downloading data for {ticker} on attempt {retries + 1}: {str(e)}")
                retries += 1
                if retries < self.MAX_RETRIES:
                    continue
                else:
                    logger.error(f"Failed to download data for {ticker} after {self.MAX_RETRIES} attempts")
                    return None, None, None

    def save_ticker_data(self, ticker: str, adj_prices: pd.DataFrame, unadj_prices: pd.DataFrame, dividends: pd.DataFrame) -> bool:
        """
        Save ticker data to Excel, preserving existing data for other tickers
        Returns: True if save was successful, False otherwise
        """
        try:
            # Initialize DataFrames
            existing_adj = pd.DataFrame()
            existing_unadj = pd.DataFrame()
            existing_div = pd.DataFrame()
            
            # Read existing data if file exists
            if os.path.exists(self.excel_path):
                try:
                    with pd.ExcelFile(self.excel_path) as xls:
                        existing_adj = pd.read_excel(xls, self.DAILY_PRICES_SHEET, index_col=0)
                        existing_unadj = pd.read_excel(xls, self.UNADJUSTED_PRICES_SHEET, index_col=0)
                        existing_div = pd.read_excel(xls, self.DIVIDENDS_SHEET, index_col=0)
                        
                        # Convert string dates to datetime.date objects
                        existing_adj.index = pd.to_datetime(existing_adj.index).date
                        existing_unadj.index = pd.to_datetime(existing_unadj.index).date
                        existing_div.index = pd.to_datetime(existing_div.index).date
                        
                        # Remove any 'Amount' column from existing dividend data
                        if 'Amount' in existing_div.columns:
                            existing_div = existing_div.drop('Amount', axis=1)
                except Exception as e:
                    logger.warning(f"Could not read existing file, creating new: {str(e)}")
            
            # Update data for this ticker
            if not existing_adj.empty:
                existing_adj[ticker] = adj_prices[ticker]
            else:
                existing_adj = adj_prices
                
            if not existing_unadj.empty:
                existing_unadj[ticker] = unadj_prices[ticker]
            else:
                existing_unadj = unadj_prices
                
            # Handle dividend data merging
            if not existing_div.empty:
                if not dividends.empty:
                    # Create a new DataFrame with all dates from both existing and new data
                    all_dates = pd.Index(sorted(set(existing_div.index) | set(dividends.index)))
                    new_div = pd.DataFrame(index=all_dates)
                    
                    # Copy existing data
                    for col in existing_div.columns:
                        if col != ticker:  # Skip the current ticker as we'll update it
                            new_div[col] = existing_div[col]
                    
                    # Add the new ticker data
                    new_div[ticker] = dividends[ticker]
                    
                    # Remove rows with all NaN values
                    existing_div = new_div.dropna(how='all')
            else:
                existing_div = dividends if not dividends.empty else pd.DataFrame()
            
            # Ensure all indexes are sorted
            existing_adj.sort_index(inplace=True)
            existing_unadj.sort_index(inplace=True)
            if not existing_div.empty:
                existing_div.sort_index(inplace=True)
            
            # Save to Excel with xlsxwriter engine
            with pd.ExcelWriter(self.excel_path, engine='xlsxwriter') as writer:
                existing_adj.to_excel(writer, sheet_name=self.DAILY_PRICES_SHEET)
                existing_unadj.to_excel(writer, sheet_name=self.UNADJUSTED_PRICES_SHEET)
                if not existing_div.empty:
                    existing_div.to_excel(writer, sheet_name=self.DIVIDENDS_SHEET)
                else:
                    pd.DataFrame().to_excel(writer, sheet_name=self.DIVIDENDS_SHEET)
                    
                # Calculate and write metrics
                calculate_and_write_metrics(existing_adj, existing_div, writer, self.CALCULATIONS_SHEET)
            
            logger.info(f"Successfully saved data for {ticker}")
            return True
            
        except PermissionError:
            logger.error(f"Permission denied: Could not save to {self.excel_path}. Please close the file if it's open.")
            return False
        except Exception as e:
            logger.error(f"Failed to save data for {ticker}: {str(e)}")
            return False

    def get_ticker_data(self, ticker: str) -> Tuple[Optional[pd.Series], Optional[pd.Series], Optional[pd.Series]]:
        """
        Get ticker data from Excel
        Returns: (daily_prices, unadjusted_prices, dividends)
        """
        try:
            with pd.ExcelFile(self.excel_path) as xls:
                daily_prices = pd.read_excel(xls, self.DAILY_PRICES_SHEET, index_col=0)
                unadj_prices = pd.read_excel(xls, self.UNADJUSTED_PRICES_SHEET, index_col=0)
                div_data = pd.read_excel(xls, self.DIVIDENDS_SHEET, index_col=0)
            
            # Convert index to datetime
            daily_prices.index = pd.to_datetime(daily_prices.index)
            unadj_prices.index = pd.to_datetime(unadj_prices.index)
            div_data.index = pd.to_datetime(div_data.index)
            
            if ticker not in daily_prices.columns:
                logger.warning(f"No data found for {ticker}")
                return None, None, None
            
            return (
                daily_prices[ticker],
                unadj_prices[ticker] if ticker in unadj_prices.columns else None,
                div_data[ticker] if ticker in div_data.columns else None
            )
            
        except Exception as e:
            logger.error(f"Error retrieving data for {ticker}: {str(e)}")
            return None, None, None
