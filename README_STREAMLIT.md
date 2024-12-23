# ETF Metrics Dashboard - Streamlit Implementation (Dec 13, 2024)

## Overview
This version adds a Streamlit-based dashboard to visualize ETF metrics from the Excel output. The dashboard matches the Excel formatting exactly and provides an interactive interface for viewing the metrics.

## Key Features Added
1. **Streamlit Dashboard**
   - Located in `/streamlit_app/metrics_test.py`
   - Displays ETF metrics with exact Excel formatting
   - Color coding: red for negative values, green for positive
   - Two-tab layout (Metrics and Correlation Analysis)

2. **Data Formatting**
   - Percentage values displayed with 1 decimal place (e.g., 1.2%)
   - Sharpe ratio with 2 decimal places
   - Shortened ETF names for better readability
   - Matches Excel formatting exactly

## Directory Structure
- `/streamlit_app/`: Contains all Streamlit-related code
  - `metrics_test.py`: Main dashboard implementation
  - `components/`: Future component files
  - `utils/`: Utility functions

## Running the Dashboard

### Production Setup (Verified Working)
```bash
# Direct execution path (preferred method)
S:/Dropbox/Scott Only Internal/Quant_Python_24/my_quant_env/Scripts/streamlit.exe run S:/Dropbox/Scott Only Internal/Quant_Python_24/XLSX_metrics_Streamlit_121324/streamlit_app/dashboard_xlsx_viewer.py
```

### Key Points
- Uses absolute paths to ensure reliability
- Directly calls streamlit.exe from my_quant_env
- No manual environment activation needed
- Preserves all environment settings

### Alternative Methods (Not Recommended)
- Manual environment activation
- Relative paths
- Shell-based activation scripts

## How to Run
1. Ensure you're in the `my_quant-env` environment
2. Navigate to project directory
3. Run: `streamlit run streamlit_app/metrics_test.py`

## Next Steps
1. Implement correlation heatmap in second tab
2. Add ticker input functionality
3. Add more interactive features and visualizations

## Known Working State
- Successfully reads and displays metrics from Excel file
- Correct number formatting and color coding
- Clean, simple interface

## Logo Implementation Notes

### What Doesn't Work
- ❌ CSS containers with width settings (unpredictable scaling)
- ❌ use_column_width parameter (insufficient control)
- ❌ Small width values (45-67px) with direct st.image() (too small)
- ❌ CSS with !important tags (doesn't override effectively)
- ❌ Placing logo outside column structure (breaks layout)

### Current Working Solution
- ✅ Using three-column layout [1,2,1]
- ✅ Logo in right column with direct width control
- ✅ Using st.image() with width=150 parameter
- ✅ No CSS containers or styling needed
- ✅ Clean, predictable scaling

### Key Learnings
- Direct width parameter in st.image() scales differently than CSS container-based approaches
- Larger width values (150px) work better with direct st.image() sizing
- Simpler approach (no containers) provides more predictable results
- Original image (1390x1090) can be displayed well without pre-processing

### Future Considerations
- May need to adjust width value if layout changes
- Could add margin-top CSS if vertical positioning needs adjustment
- Keep monitoring Streamlit's image handling in future releases

## Layout Implementation Notes (*** DO NOT CHANGE LAYOUT ***)

### Current Working Layout (v4_test2)
- ✅ Three-column header layout [1,2,1]
- ✅ Logo in right column with width=150
- ✅ Proper banner text styling and spacing
- ✅ Correct metrics table formatting
- ✅ Two-tab structure for Metrics and Correlation

### Protected Layout Sections
1. **Header Section**
   - Three-column ratio [1,2,1] is optimized
   - Banner text styling and spacing is finalized
   - Logo placement and sizing is fixed

2. **Input Section**
   - Two-column layout [3,1] for ticker input
   - Button placement and styling finalized

3. **Table Display**
   - Font sizes and alignments optimized
   - Color coding for positive/negative values
   - Column spacing set for readability

4. **Critical Formatting**
   - Percentage values must be multiplied by 100 for display
   - All percentages formatted to one decimal place
   - Sharpe ratio formatted to two decimal places
   - Excel/Dashboard format consistency must be maintained

### What Doesn't Work (DO NOT ATTEMPT)
- ❌ Changing column ratios
- ❌ Modifying banner text styling
- ❌ Adjusting logo placement
- ❌ Altering table display format
- ❌ Changing percentage formatting method

## Table Styling Limitations

### What Doesn't Work
- ❌ Header alignment/centering (Streamlit limitation)
- ❌ Custom CSS for table headers
- ❌ Direct HTML styling injection
- ❌ Custom CSS classes for tables
- ❌ Header font customization

### Current Working Solution (*** DO NOT MODIFY ***)
- ✅ Pandas-based number formatting with 100x multiplier for percentages
- ✅ Color coding for positive/negative values
- ✅ Basic table structure and layout
- ✅ Consistent decimal places
- ✅ Clean, readable display

## Critical Code Sections

### Percentage Formatting
The percentage formatting section in `dashboard_xlsx_viewer_v4_test2.py` is now protected and verified working. This section handles the conversion of Excel decimal values to properly formatted percentages.

**How it works:**
1. Excel stores percentages as decimals (e.g., 0.29 for 29%)
2. When pandas reads these values, they come in as decimals (e.g., 0.0029)
3. The code multiplies by 10000 to convert from decimal to percentage display format
4. Example: 0.0029 (from Excel) * 10000 = 29.0%

**Protected Columns:**
- Day%
- MTD%
- YTD%
- 2023%
- 2022%
- Volatility
- Max_Drawdown
- %Yield

**⚠️ WARNING:**
- DO NOT modify the protected percentage formatting section
- DO NOT change the multiplication factor of 10000
- DO NOT modify the formatting string "{x:.1f}%"
- DO NOT change the column list without approval
- Changes to this section require thorough testing and validation

## Data Reading Implementation
- Reads from existing Excel files in test_output directory
- Uses most recent file based on modification time
- Supports filtering by comma-separated tickers
- Preserves all Excel formatting and calculations
- Read-only operation with no file modifications

### File Access
- Location: `Basic_XLSX_PlusCalc_Restored_120424/test_output`
- Format: `.xlsx` files with 'Metrics' sheet
- Selection: Latest file by modification time
- Error handling for missing/invalid files

### Ticker Input
- Text input field for comma-separated tickers
- Case-insensitive matching
- Shows all data if no tickers entered
- Clear error messages for invalid states

## Project Status as of Dec 14, 2024 21:40 EST

### Working Features
- ETF name resolution using yfinance API
- Right-aligned numeric columns in metrics table
- Left-aligned text columns (Ticker, Name)
- Proper percentage formatting with one decimal place
- Error handling for failed data fetches
- Correlation analysis tab (placeholder)

### Known Issues and Limitations
1. **Number of Tickers**: Current implementation may have performance issues with large number of tickers
   - Need to establish and test upper limit
   - Consider pagination or scrolling for large datasets
   - Monitor yfinance API rate limits

### Recent Critical Changes
1. **ETF Name Resolution** (Dec 14, 2024)
   - Switched from hardcoded dictionary to dynamic yfinance lookup
   - Added fallback to ticker symbol if lookup fails
   - See Change Log section for reversion instructions if needed

2. **Table Formatting** (Dec 14, 2024)
   - Implemented consistent column alignment
   - Numeric columns: right-aligned
   - Text columns: left-aligned
   - Using Streamlit's native column configuration for stability

### Backup Information
- **Latest Backup**: December 14, 2024 21:40 EST
- **Backup Location**: `S:\Dropbox\Scott Only Internal\Quant_Python_24\XLSX_metrics_Streamlit_Backup_121424`
- **Version**: v4_test2 (Working Version)
- **State**: Stable, production-ready with documented limitations

## Change Log - Important Modifications

#### 2024-12-14: ETF Name Resolution Change
**File Modified**: `src/models/metrics_writer.py`
**Change Type**: Potentially Reversible Change

**What Changed**:
- Removed hardcoded ticker_names dictionary
- Added dynamic ETF name lookup using yfinance
- Added error handling for name lookup failures

**Why**:
- To fix QQQ name display issue
- To make ETF name resolution more dynamic and maintainable

**How to Revert**:
```python
# Original code used this dictionary:
ticker_names = {
    'SPY': 'SPDR S&P 500 ETF Trust',
    'JNK': 'SPDR Bloomberg High Yield Bond ETF',
    'IEI': 'iShares 3-7 Year Treasury Bond ETF'
}

# And this line for name lookup:
'Name': ticker_names.get(ticker, ticker),  # Use full name if available
```

To revert:
1. Remove the new yfinance import
2. Remove the ETF info lookup code block
3. Restore the ticker_names dictionary
4. Replace the dynamic name lookup with the original dictionary lookup

**Potential Issues to Watch**:
- Additional yfinance API calls may affect performance
- Network dependency for name resolution
- May need to revert if:
  1. Performance degrades significantly
  2. Network issues impact reliability
  3. yfinance API changes affect name lookup

## Upcoming Features & Improvements

### 1. Relative Performance Graph
- Add interactive chart showing relative performance between assets
- Allow selection of benchmark (e.g., SPY)
- Include time period selector (YTD, 1Y, 3Y, etc.)
- Implement proper scaling and legend

### 2. Footnotes Integration
- Restore footnotes functionality from previous version
- Add tooltips for metric explanations
- Include data source and calculation methodology
- Add timestamp of last data update

### 3. Metrics Enhancement
- Improve existing metrics display and formatting
- Add sorting capabilities for all columns
- Implement conditional formatting (color coding)
- Add filters for asset types (ETFs, Stocks, CEFs)

### 4. Additional Asset Class Metrics
**Stocks:**
- P/E Ratio
- Market Cap
- Dividend Growth Rate
- Beta
- Sector/Industry

**CEFs (Closed-End Funds):**
- Premium/Discount to NAV
- Distribution Rate
- Coverage Ratio
- Leverage Ratio
- Management Fee

### Current State (Dec 14, 2024)

### Working Features
- ✅ Excel metrics reading and display
- ✅ Percentage formatting fixed and protected (multiplying by 10000)
- ✅ Batch file for easy launch
- ✅ Logo and layout finalized
- ✅ Correlation matrix tab

### Critical Protected Sections
1. Percentage Formatting in `dashboard_xlsx_viewer_v4_test2.py`
   - DO NOT modify multiplication factor (10000)
   - DO NOT change formatting strings
   - See protected code section for details

### Latest Backup
- Full backup created at: `XLSX_metrics_Streamlit_Backup_121424`
- Includes all working code and documentation

### Next Development Steps
1. Relative Performance Graph (Priority)
   - Start with `streamlit_app/components/charts.py`
   - Use existing Excel data structure
   - Consider using Plotly for interactive charts

### Active Working Directory
```
S:\Dropbox\Scott Only Internal\Quant_Python_24\XLSX_metrics_Streamlit_121324
```

### Launch Command
```
S:\Dropbox\Scott Only Internal\Quant_Python_24\XLSX_metrics_Streamlit_121324\run_dashboard.bat
```

## Running the Dashboard
A batch file has been created for easy launch:
```
Location: S:\Dropbox\Scott Only Internal\Quant_Python_24\XLSX_metrics_Streamlit_121324\run_dashboard.bat
```
Double-click the batch file or create a desktop shortcut to launch the dashboard.

## Latest Updates (Dec 14, 2024)
- Logo implementation finalized with correct sizing
- Dashboard layout optimized with three-column design
- Documentation updated with table styling limitations
- Backup planned to preserve current state

## Backup Information
- Location: `S:\Dropbox\Scott Only Internal\Quant_Python_24\XLSX_metrics_Streamlit_Backup_121424`
- Contents: Complete working state including:
  - Streamlit dashboard implementation
  - Logo and layout improvements
  - All supporting files and documentation

## Dependencies
- streamlit
- pandas
- All existing project dependencies

## Notes
- This implementation preserves all existing code functionality
- Streamlit interface is separate from core calculation logic
- Excel output remains the source of truth for data

## File Naming Convention
- Excel files are named with timestamp and up to first 3 tickers
- Format: `dashboard_data_YYYYMMDD_HHMM_TICKER1_TICKER2_TICKER3.xlsx`
- When processing more than 3 tickers, only first 3 are used in filename

## Future Expansion Notes (15+ Tickers)
1. Memory Management:
   - Batch processing in groups of 10 tickers
   - Memory clearing between batches
   - Memory usage monitoring
2. File Management:
   - Split into multiple Excel files (one per 15 tickers)
   - File size monitoring
3. Performance:
   - Parallel processing for downloads
   - Progress tracking per batch

## What Doesn't Work (DO NOT ATTEMPT)
- ❌ Changing column ratios
- ❌ Modifying banner text styling
- ❌ Adjusting logo placement
- ❌ Altering table display format
- ❌ Changing input field layout
