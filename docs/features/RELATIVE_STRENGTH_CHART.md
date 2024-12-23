# Relative Strength Chart Documentation 🟢

## Overview
The relative strength chart module provides comparative performance visualization for multiple tickers, indexed to a base value of 100 at the start date.

## Features
- Uses adjusted close prices from 'Daily Prices' sheet
- Default 3-year window (configurable)
- Base 100 indexing from start date
- Interactive legend for ticker selection
- Unified hover tooltips
- Matches stockcharts.com style presentation

## Data Source
- Sheet: 'Daily Prices' (contains adjusted close prices)
- Format: Excel file with date index and ticker columns
- No data manipulation required - uses raw adjusted prices

## Chart Specifications
### Visual Style
- White background
- Light grey grid
- Clear axis labels
- Horizontal legend at top
- Line width: 2px
- Percentage values with 1 decimal place

### Interactivity
- Click legend to show/hide tickers
- Hover shows all ticker values at x-position
- Tooltip format: "Ticker: XX.X%"

### Time Window
- Default: 3 years
- Minimum: 3 months
- Uses most recent data point as end date

## Usage Guidelines
1. **Protected Code**
   - Core calculation logic marked as "WORKING ONLY"
   - Changes require explicit permission
   - No timestamps/timezone modifications

2. **Data Requirements**
   - Must use adjusted close prices
   - Excel file must contain 'Daily Prices' sheet
   - Date column must be first column

3. **Integration Rules**
   - Place at bottom of first dashboard page
   - Maintain existing dashboard layout
   - No changes to Excel processing
   - Keep as standalone module

## Error Handling
- Graceful handling of missing data
- Clear error messages in logs
- No data points shown except at start of time period

## Dependencies
- Plotly for charting
- Pandas for data handling
- No additional external dependencies

## Testing
- Test with varying numbers of tickers
- Verify calculations match expected results
- Check all interactive features
- Ensure proper error handling

## Recent Updates (December 16, 2024)

### Chart Improvements
- Changed chart title to "Adjusted Close (Base 100)"
- Optimized date axis formatting with quarterly ticks and limited labels
- Added dynamic time range selector with options:
  - 3M (3 months)
  - 6M (6 months)
  - 1Y (1 year)
  - 3Y (3 years, default)
  - Max (all available data)

### Latest Backup
- Location: XLSX_Plot_Streamlit_Backup_121524
- Date: December 16, 2024
- Contains: All recent chart improvements and axis optimizations
