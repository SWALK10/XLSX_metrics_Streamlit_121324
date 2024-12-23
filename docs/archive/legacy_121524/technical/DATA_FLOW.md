# Data Flow Documentation

## Overview
The system downloads and processes stock data from Yahoo Finance (yfinance) and saves it to Excel files. The system is designed for reliability and consistent output formatting.

## Important Note on Timestamps
- NO timestamps or timezone data in any data processing, calculations, or storage
- NO timezone conversions in data handling
- All dates must be date-only format without time components
- Exception: File naming ONLY uses timestamps for tracking purposes
  - Format: `dashboard_data_YYYYMMDD_HHMM_tickers.xlsx`
  - This is purely for file organization and version tracking
  - Does NOT affect any data inside the files

## Core Components

### 1. Excel Manager (`src/data/excel_manager.py`)
- Handles file operations and data management
- Creates uniquely named files with timestamps
- Manages sheet creation and formatting
- Coordinates data download and metrics calculation

### 2. Performance Metrics (`src/models/performance_metrics.py`)
- Calculates all financial metrics
- Handles risk and return calculations
- Uses consistent calculation methods
- Provides error handling for edge cases

### 3. Metrics Writer (`src/models/metrics_writer.py`)
- Writes calculated metrics to Excel
- Manages formatting and layout
- Ensures consistent output structure
- Handles multi-ticker calculations

## Data Flow Steps

### 1. Initialization
- ExcelManager created with output directory
- Timestamp and ticker list used for unique filename
- Empty Excel file created with required sheets:
  - Daily Prices
  - Unadjusted Prices
  - Dividends
  - Metrics

### 2. Data Download (per ticker)
1. **Price Data**
   - Download adjusted price history (2020-01-01 onward)
   - Download unadjusted price history
   - Convert all dates to date-only format (no timezones)

2. **Dividend Data**
   - Fetch dividend history
   - Filter to relevant date range
   - Remove any zero-value dividends
   - Convert to date-only format

### 3. Data Processing
1. **Price Data**
   - Create single-column DataFrames per ticker
   - Ensure consistent date format
   - Sort chronologically

2. **Dividend Data**
   - Create single-column DataFrames per ticker
   - Remove duplicates
   - Sort chronologically

### 4. Metrics Calculation
1. **Return Metrics**
   - Daily returns
   - Month-to-date returns
   - Year-to-date returns
   - Calendar year returns (2022, 2023)

2. **Risk Metrics**
   - Volatility (annualized)
   - Sharpe ratio (using 3% risk-free rate)
   - Maximum drawdown

3. **Income Metrics**
   - Trailing 12-month dividend yield
   - Based on latest price and TTM dividends

### 5. Excel Output
1. **File Creation**
   - New file with timestamp and tickers
   - All required sheets initialized
   - Proper date formatting applied

2. **Data Writing**
   - Write prices to respective sheets
   - Write dividends with proper formatting
   - Calculate and write all metrics
   - Apply consistent formatting

## Excel File Reading (Streamlit)

### File Location
- Base path: `S:/Dropbox/Scott Only Internal/Quant_Python_24/Basic_XLSX_PlusCalc_Restored_120424/test_output`
- Reads most recent Excel file based on file modification time
- No direct file writing or modification from Streamlit

### Ticker Filtering Process
1. **File Selection**
   - Scans directory for .xlsx files
   - Uses `os.path.getmtime()` to find latest file
   - Handles missing files with proper error messages

2. **Data Reading**
   - Reads 'Metrics' sheet only
   - No modification of source data
   - Preserves all formatting and calculations

3. **Ticker Filtering**
   - Accepts comma-separated ticker input
   - Converts tickers to uppercase
   - Filters DataFrame using `df['Ticker'].isin(tickers)`
   - Returns filtered or full dataset based on input

4. **Error Handling**
   - Handles missing files gracefully
   - Reports read errors to user
   - Returns None for invalid states

## Development Environment

### Streamlit Execution
- **Verified Working Path**:
  ```bash
  S:/Dropbox/Scott Only Internal/Quant_Python_24/my_quant_env/Scripts/streamlit.exe run S:/Dropbox/Scott Only Internal/Quant_Python_24/XLSX_metrics_Streamlit_121324/streamlit_app/dashboard_xlsx_viewer.py
  ```

### Critical Notes
- Always use absolute paths
- Direct streamlit.exe execution
- Environment: my_quant_env
- No manual activation required

### Path Structure
- Environment: `/my_quant_env/Scripts/streamlit.exe`
- Application: `/XLSX_metrics_Streamlit_121324/streamlit_app/`
- Main file: `dashboard_xlsx_viewer.py` or `dashboard_xlsx_viewer_v2.py`

## Code Modification Guidelines

### 1. Code Preservation Rules
- Sections marked with "DO NOT MODIFY" comments must remain unchanged
- Working code should never be rewritten unless explicitly requested
- Optimizations and improvements must be discussed before implementation
- Each file should maintain a clear record of working sections

### 2. Version Control Practice
- Create annotated versions (e.g., `*_wnotes.py`) before major changes
- Use clear section markers to indicate protected code blocks
- Document why each section should not be modified
- Keep reference copies of working versions

### 3. Change Management
- Focus only on new functionality requested
- Add new features by inserting into designated sections
- Preserve existing formatting and styling
- Maintain a checklist of allowed vs. prohibited changes

### 4. Development Process
- Start with working code as base
- Add ONLY necessary new functionality
- Review diffs against working version before implementing
- Explain WHY any working code needs to be modified

## Metrics Details

### Currently Implemented Metrics
| Metric | Description | Calculation Method |
|--------|-------------|-------------------|
| Ticker | Symbol | Direct from input |
| Name | Full ETF name | Lookup table |
| %Yield | TTM Dividend Yield | TTM Dividends / Current Price |
| Sharpe | Sharpe Ratio | (Return - Risk Free) / Volatility |
| Day% | Daily Return | (Today - Yesterday) / Yesterday |
| MTD% | Month-to-Date | (Current - Month Start) / Month Start |
| YTD% | Year-to-Date | (Current - Year Start) / Year Start |
| 2023% | Calendar Year 2023 | (Year End - Year Start) / Year Start |
| 2022% | Calendar Year 2022 | (Year End - Year Start) / Year Start |
| Volatility | Annualized Vol | Std Dev * √252 |
| Max_Drawdown | Maximum Drawdown | (Peak - Trough) / Peak |

### Formatting Standards
- Percentages: 1 decimal place (XX.X%)
- Sharpe ratio: 2 decimal places (XX.XX)
- Numeric columns: Right-aligned
- Text columns: Left-aligned

## Error Handling

### 1. Data Download
- Retry logic for API failures
- Graceful handling of missing data
- Logging of all download attempts

### 2. Calculations
- Default to 0.0 for failed calculations
- Log warnings for calculation issues
- Continue processing on partial failures

### 3. File Operations
- Handle file permission errors
- Create new file if existing unreadable
- Validate all writes

## Testing

### 1. Unit Tests
Located in `tests/test_metrics_calculations.py`:
- Return calculation validation
- Risk metric bounds checking
- Yield calculation verification
- Calendar year return accuracy

### 2. Integration Test
Located in `tests/test_etf_metrics.py`:
- Full workflow testing
- Multi-ticker processing
- Output file verification

## Known Issues and Solutions
1. Timezone handling: Resolved by converting to date-only
2. Yield calculation: Now uses trailing 12-month dividends
3. ETF names: Added proper lookup table
4. Calendar returns: Fixed calculation method
