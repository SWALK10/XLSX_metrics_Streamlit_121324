# Calculation Rules and Formulas

## Overview
This document details the exact calculation methods for each metric in the system.

## Return Calculations

### 1. Daily Return (Day%)
```python
daily_return = (price_today / price_yesterday) - 1
```
- Uses adjusted closing prices
- Expressed as percentage
- One decimal place

### 2. Month-to-Date Return (MTD%)
```python
mtd_return = (current_price / month_start_price) - 1
```
- Month start = first trading day
- Uses adjusted prices
- One decimal place

### 3. Year-to-Date Return (YTD%)
```python
ytd_return = (current_price / year_start_price) - 1
```
- Year start = first trading day of current year
- Uses adjusted prices
- One decimal place

### 4. Calendar Year Returns (2023%, 2022%)
```python
calendar_return = (year_end_price / year_start_price) - 1
```
- Year start = first trading day of year
- Year end = last trading day of year
- Uses adjusted prices
- One decimal place

## Risk Metrics

### 1. Volatility
```python
daily_returns = price.pct_change()
annual_vol = daily_returns.std() * sqrt(252)
```
- Annualized using 252 trading days
- Based on daily returns
- One decimal place

### 2. Sharpe Ratio
```python
excess_return = annualized_return - risk_free_rate
sharpe = excess_return / volatility
```
- Risk-free rate = 3%
- Uses annualized values
- Two decimal places

### 3. Maximum Drawdown
```python
rolling_max = price.expanding().max()
drawdown = (price - rolling_max) / rolling_max
max_drawdown = drawdown.min()
```
- Calculated on adjusted prices
- Expressed as percentage
- One decimal place

## Income Metrics

### 1. Trailing 12-Month Yield
```python
ttm_dividends = sum(dividends[last_12_months])
current_price = latest_adjusted_close
yield = ttm_dividends / current_price
```
- Uses actual dividend payments
- Based on trailing 12 months
- One decimal place

## Data Requirements

### 1. Price Data
- Daily frequency
- Adjusted for splits/dividends
- From 2020-01-01 to present
- No missing values allowed

### 2. Dividend Data
- Actual payment dates
- Adjusted for splits
- Filtered for non-zero values
- From 2020-01-01 to present

## Formatting Rules

### 1. Percentages
```
Format: XX.X%
Examples: 12.3%, -5.4%, 0.0%
```

### 2. Ratios
```
Format: XX.XX
Examples: 1.23, -0.45, 0.00
```

### 3. Names
```
Format: Full ETF Name
Examples: "SPDR S&P 500 ETF Trust"
```

## Error Handling

### 1. Missing Data
- Return 0.0 for calculations
- Log warning message
- Continue processing

### 2. Invalid Results
- Cap at reasonable bounds
- Log error message
- Use fallback value

### 3. Date Ranges
- Skip incomplete periods
- Log warning message
- Use available data
