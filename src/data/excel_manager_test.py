"""
Test version of Excel Manager for experimenting with NA handling
Focus on XLSX writing with proper handling of different history lengths
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import yfinance as yf
import logging
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExcelManagerTest:
    """Test version of Excel Manager focusing on NA handling"""
    
    DAILY_PRICES_SHEET = 'Daily Prices'
    UNADJUSTED_PRICES_SHEET = 'Unadjusted Prices'
    DIVIDENDS_SHEET = 'Dividends'
    
    def __init__(self, output_dir: str):
        """Initialize with output directory"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def download_ticker_data(self, ticker: str) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Download data for a single ticker from 2020-01-01"""
        try:
            # Set date range
            start_date = '2020-01-01'
            end_date = date.today().strftime('%Y-%m-%d')
            
            # Download data
            stock = yf.Ticker(ticker)
            
            # Get adjusted price data
            adj_hist = stock.history(start=start_date, end=end_date, auto_adjust=True)
            if adj_hist.empty:
                logger.warning(f"No data found for {ticker}")
                return None, None, None
                
            # Get unadjusted price data
            unadj_hist = stock.history(start=start_date, end=end_date, auto_adjust=False)
            
            # Get dividend data
            try:
                actions_div = stock.actions[['Dividends']].loc[start_date:end_date]
                dividends = actions_div[actions_div['Dividends'] > 0]
                dividends.columns = [ticker]
            except Exception as div_err:
                logger.warning(f"Error fetching dividends for {ticker}: {str(div_err)}")
                dividends = pd.DataFrame(columns=[ticker])
            
            # Convert index to date (not datetime)
            adj_hist.index = adj_hist.index.date
            unadj_hist.index = unadj_hist.index.date
            if not dividends.empty:
                dividends.index = dividends.index.date
            
            # Create single-column dataframes
            adj_prices = pd.DataFrame({ticker: adj_hist['Close']})
            unadj_prices = pd.DataFrame({ticker: unadj_hist['Close']})
            
            logger.info(f"Downloaded {len(adj_hist)} days of history for {ticker}")
            return adj_prices, unadj_prices, dividends
            
        except Exception as e:
            logger.error(f"Error downloading {ticker}: {str(e)}")
            return None, None, None
    
    def save_ticker_data(self, ticker: str, adj_df: pd.DataFrame, unadj_df: pd.DataFrame, div_df: pd.DataFrame) -> bool:
        """Save ticker data to Excel file"""
        try:
            # Convert index to datetime.date for consistent comparison
            adj_df.index = pd.to_datetime(adj_df.index).date
            unadj_df.index = pd.to_datetime(unadj_df.index).date
            if not div_df.empty:
                div_df.index = pd.to_datetime(div_df.index).date

            # Load existing data if available
            excel_path = os.path.join(self.output_dir, self.get_current_excel_name())
            if os.path.exists(excel_path):
                xls = pd.ExcelFile(excel_path)
                sheets = xls.sheet_names

                if self.DAILY_PRICES_SHEET in sheets:
                    existing_adj = pd.read_excel(xls, self.DAILY_PRICES_SHEET, index_col=0, parse_dates=True)
                    existing_adj.index = pd.to_datetime(existing_adj.index).date
                    if ticker in existing_adj.columns:
                        # Update existing data
                        mask = ~existing_adj.index.isin(adj_df.index)
                        existing_adj.loc[mask, ticker] = pd.NA
                        adj_df = pd.concat([existing_adj[ticker].to_frame(), adj_df[ticker].to_frame()]).sort_index()
                        adj_df = adj_df[~adj_df.index.duplicated(keep='last')]

                if self.UNADJUSTED_PRICES_SHEET in sheets:
                    existing_unadj = pd.read_excel(xls, self.UNADJUSTED_PRICES_SHEET, index_col=0, parse_dates=True)
                    existing_unadj.index = pd.to_datetime(existing_unadj.index).date
                    if ticker in existing_unadj.columns:
                        mask = ~existing_unadj.index.isin(unadj_df.index)
                        existing_unadj.loc[mask, ticker] = pd.NA
                        unadj_df = pd.concat([existing_unadj[ticker].to_frame(), unadj_df[ticker].to_frame()]).sort_index()
                        unadj_df = unadj_df[~unadj_df.index.duplicated(keep='last')]

                if self.DIVIDENDS_SHEET in sheets and not div_df.empty:
                    existing_div = pd.read_excel(xls, self.DIVIDENDS_SHEET, index_col=0, parse_dates=True)
                    existing_div.index = pd.to_datetime(existing_div.index).date
                    if ticker in existing_div.columns:
                        mask = ~existing_div.index.isin(div_df.index)
                        existing_div.loc[mask, ticker] = pd.NA
                        div_df = pd.concat([existing_div[ticker].to_frame(), div_df[ticker].to_frame()]).sort_index()
                        div_df = div_df[~div_df.index.duplicated(keep='last')]

                xls.close()

            # Write updated data back to Excel
            with pd.ExcelWriter(excel_path, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
                adj_df.to_excel(writer, sheet_name=self.DAILY_PRICES_SHEET, na_rep='=NA()')
                unadj_df.to_excel(writer, sheet_name=self.UNADJUSTED_PRICES_SHEET, na_rep='=NA()')
                if not div_df.empty:
                    div_df.to_excel(writer, sheet_name=self.DIVIDENDS_SHEET, na_rep='=NA()')

            logger.info(f"Successfully saved data for {ticker}")
            return True

        except Exception as e:
            logger.error(f"Failed to save data for {ticker}: {str(e)}")
            return False

    def write_test_file(self, tickers: List[str]):
        """Test function to write Excel with proper NA handling"""
        # Download data for each ticker
        adj_data = {}
        unadj_data = {}
        div_data = {}
        
        for ticker in tickers:
            adj_df, unadj_df, div_df = self.download_ticker_data(ticker)
            if adj_df is not None:
                # Ensure index is date type
                adj_df.index = pd.to_datetime(adj_df.index).date
                unadj_df.index = pd.to_datetime(unadj_df.index).date
                if not div_df.empty:
                    div_df.index = pd.to_datetime(div_df.index).date
                
                adj_data[ticker] = adj_df[ticker]
                unadj_data[ticker] = unadj_df[ticker]
                if not div_df.empty:
                    div_data[ticker] = div_df[ticker]
        
        if not adj_data:
            logger.error("No data downloaded")
            return
            
        # Create DataFrames with all tickers
        adj_df = pd.DataFrame(adj_data)
        unadj_df = pd.DataFrame(unadj_data)
        div_df = pd.DataFrame(div_data)
        
        # Write to Excel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        excel_path = os.path.join(self.output_dir, f"test_data_{timestamp}.xlsx")
        
        with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
            # Write each sheet with NA handling
            adj_df.to_excel(writer, sheet_name=self.DAILY_PRICES_SHEET, na_rep='=NA()')
            unadj_df.to_excel(writer, sheet_name=self.UNADJUSTED_PRICES_SHEET, na_rep='=NA()')
            if not div_df.empty:
                div_df.to_excel(writer, sheet_name=self.DIVIDENDS_SHEET, na_rep='=NA()')
            else:
                pd.DataFrame().to_excel(writer, sheet_name=self.DIVIDENDS_SHEET)
        
        logger.info(f"Test file written to {excel_path}")
        return excel_path

def run_test(tickers: List[str], output_dir: str):
    """Run a test with specified tickers"""
    test_mgr = ExcelManagerTest(output_dir)
    return test_mgr.write_test_file(tickers)
