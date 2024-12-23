"""
Metrics Writer Module

This module calculates financial performance metrics and writes them to Excel using xlsxwriter.
Designed for reliability, consistency, and maintainable output formatting.

Key Features:
- Independent metric calculations to prevent cascading failures
- Consistent Excel formatting using xlsxwriter engine
- Robust error handling and logging
- Full workbook writing in single operation (no append mode)

Metrics Calculated:
- Ticker: Stock symbol
- Name: Full security name
- %Yield: Current dividend yield (trailing 12 months)
- Sharpe 2Y: Two-year Sharpe ratio (using BIL ETF risk-free rate)
- Day%: Daily return percentage
- 1MTH%: One month return percentage
- YTD%: Year-to-date return percentage
- 2023%: Calendar year 2023 return
- 2022%: Calendar year 2022 return
- Volatility: Annualized volatility
- Max_Drawdown: Maximum drawdown percentage

Excel Formatting Rules:
- Percentage metrics: One decimal place (0.0%)
- Sharpe ratio: Two decimal places (0.00)
- All numeric columns: Right-aligned
- Text columns: Left-aligned
- No special formatting flags or warnings

Dependencies:
- pandas: Data manipulation and Excel writing
- numpy: Numerical calculations
- xlsxwriter: Excel formatting and output
- datetime: Date handling
- logging: Error and operation logging
- yfinance: ETF name lookup

Known Issues:
- MTD% calculation needs refinement for proper decimal handling
"""
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
from .performance_metrics import PerformanceMetrics
import os

def calculate_and_write_metrics(price_df, dividend_df, writer, sheet_name='Metrics'):
    """
    Calculate all metrics and write to Excel.
    Each metric is calculated independently so if one fails, others will still populate.
    All percentage metrics formatted as XX.X%
    """
    if price_df.empty:
        print("DEBUG: No price data available for metrics calculation")
        return

    # Initialize performance metrics calculator
    perf = PerformanceMetrics()
    
    try:
        # Ensure index is datetime for year filtering
        price_df.index = pd.to_datetime(price_df.index)
        if not dividend_df.empty:
            dividend_df.index = pd.to_datetime(dividend_df.index)
        
        # Calculate metrics for all tickers
        all_metrics_list = []
        for ticker in price_df.columns:
            print(f"DEBUG: Calculating metrics for {ticker}")
            
            # Get ETF info from yfinance
            try:
                ticker_info = yf.Ticker(ticker).info
                etf_name = ticker_info.get('longName', ticker)
            except Exception as e:
                print(f"DEBUG: Error getting name for {ticker}: {str(e)}")
                etf_name = ticker  # Fallback to ticker if name lookup fails
            
            # Calculate all metrics using performance_metrics
            metrics = perf.calculate_all_metrics(price_df[ticker])
            print(f"DEBUG: Raw metrics for {ticker}: {metrics}")
            
            # Calculate trailing 12-month yield if dividend data available
            annual_yield = 0.0
            if not dividend_df.empty and ticker in dividend_df.columns:
                try:
                    latest_price = price_df[ticker].iloc[-1]
                    last_date = price_df.index[-1]
                    one_year_ago = last_date - pd.DateOffset(years=1)
                    ttm_divs = dividend_df[ticker][dividend_df.index >= one_year_ago].sum()
                    annual_yield = (ttm_divs / latest_price) if latest_price else 0.0
                except Exception as e:
                    print(f"DEBUG: Error calculating yield for {ticker}: {str(e)}")

            # Calculate calendar year returns
            cy_2023 = 0.0
            cy_2022 = 0.0
            
            # 2023 return
            data_2023 = price_df[ticker][price_df.index.year == 2023]
            if not data_2023.empty:
                cy_2023 = (data_2023.iloc[-1] / data_2023.iloc[0] - 1)
            
            # 2022 return
            data_2022 = price_df[ticker][price_df.index.year == 2022]
            if not data_2022.empty:
                cy_2022 = (data_2022.iloc[-1] / data_2022.iloc[0] - 1)

            # Create metrics dictionary in specific order
            ticker_metrics = {
                'Ticker': ticker,
                'Name': etf_name,
                '%Yield': annual_yield,
                'Sharpe 2Y': metrics.get('sharpe_2y', 0.0),
                'Day%': metrics.get('daily_return', 0.0),
                '1MTH%': metrics.get('one_month_return', 0.0),
                'YTD%': metrics.get('ytd_return', 0.0),
                '2023%': cy_2023,
                '2022%': cy_2022,
                'Volatility': metrics.get('volatility', 0.0),
                'Max_Drawdown': metrics.get('max_drawdown', 0.0)
            }
            print(f"DEBUG: Created metrics dictionary for {ticker}: {ticker_metrics}")
            all_metrics_list.append(ticker_metrics)

        # Convert all metrics to DataFrame preserving column order
        metrics_df = pd.DataFrame(all_metrics_list)
        print(f"DEBUG: Created metrics DataFrame with columns: {metrics_df.columns.tolist()}")
        
        # Write to Excel with formatting
        metrics_df.to_excel(writer, sheet_name=sheet_name, index=False)
        worksheet = writer.sheets[sheet_name]
        print(f"DEBUG: Successfully wrote metrics DataFrame to sheet: {sheet_name}")
        
        # Format columns
        for idx, col in enumerate(metrics_df.columns):
            # Set column width
            worksheet.set_column(idx, idx, 15)
            
            # Format percentage columns with one decimal place
            if '%' in col or col in ['Volatility', 'Max_Drawdown']:
                worksheet.set_column(idx, idx, 15, writer.book.add_format({'num_format': '0.0%'}))
            # Format Sharpe ratio with 2 decimal places
            elif col == 'Sharpe 2Y':
                worksheet.set_column(idx, idx, 15, writer.book.add_format({'num_format': '0.00'}))
        
        print(f"DEBUG: Successfully wrote metrics for all tickers")
        return True
        
    except Exception as e:
        print(f"DEBUG: Error calculating/writing metrics: {str(e)}")
        return False
