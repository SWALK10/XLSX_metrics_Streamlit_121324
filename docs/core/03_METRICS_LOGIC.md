# Calculations Documentation 

[Content migrated from technical/CALCULATIONS.md and updated for current structure]

## Metric Calculations

### Performance Metrics
- **Returns**: Calculated using close prices
  - Daily Return: (Current Close - Previous Close) / Previous Close
  - Monthly Return: Last 30 calendar days
  - YTD Return: From January 1st to current date
  - Annual Returns: Calendar year returns (2023, 2022)

### Risk & Performance Ratios
- **Sharpe Ratio Implementation** [WORKING ONLY - Change with Permission]
  - Data Requirements:
    - Exactly 504 trading days (2 years) of data
    - Uses most recent data if more is available
  - Calculation Flow:
    1. Calculate daily returns: `daily_returns = prices.pct_change()`
    2. Get risk-free rate from BIL ETF (falls back to 3% if unavailable)
    3. Convert annual risk-free rate to daily: `daily_rf_rate = annual_rate / 252`
    4. Calculate daily excess returns: `excess_returns = daily_returns - daily_rf_rate`
    5. Calculate Sharpe components:
       - Mean of excess returns: `excess_returns.mean()`
       - Standard deviation of daily returns (not excess): `daily_returns.std()`
    6. Calculate daily Sharpe: `daily_sharpe = excess_returns.mean() / daily_returns.std()`
    7. Annualize: `sharpe = daily_sharpe * sqrt(252)`
    8. Round to 2 decimal places
  - Risk-Free Rate Source:
    - Primary: BIL ETF 2-year dividend yield
    - Fallback: 3% annual rate if BIL data unavailable
  - Implementation Notes:
    - Calculation verified for multi-ticker processing
    - DO NOT modify calculation without explicit permission
    - Returns empty metrics if insufficient data (<504 days)

### Volatility Metrics
- **Annualized Volatility**
  - Uses daily returns standard deviation
  - Annualized using sqrt(252)
  - Based on same 504-day window as Sharpe

### Value at Risk (VaR)
- 95% confidence level
- Based on empirical percentile of daily returns
- Uses same 504-day window as other metrics

### Maximum Drawdown
- Calculated over entire price history
- Formula: (Peak - Trough) / Peak
- Expressed as positive percentage

### Dividend Metrics
- **Yield Calculation**
  - Based on trailing 12-month dividends
  - Formula: (Sum of last 12 months dividends) / Current Price

### Data Processing Notes
- All calculations use adjusted close prices for accuracy
- Missing data points are marked as N/A
- Market data updates daily via Yahoo Finance API

## Working State
All calculations verified and functional as of 2024-12-15

## Implementation Details
- Core calculations in `src/models/performance_metrics.py`
- Data processing in `src/data/processor.py`
- Output formatting in `src/utils/excel_formatter.py`
