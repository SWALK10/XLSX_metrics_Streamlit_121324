# Quick Start Guide

## First Time Setup

1. **Check Python Installation**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Directory Structure**
   ```
   S:/Dropbox/Scott Only Internal/Quant_Python_24/Basic_XLSX_PlusCalc_Restored_120424/
   ├── src/               # Source code
   ├── test_output/      # Generated Excel files
   └── tests/            # Test files
   ```

## Running the Code

### Method 1: Run Main Script
```bash
cd src
python etf_analytics.py
```

### Method 2: Run Tests
```bash
cd tests
python test_etf_metrics.py
```

## Expected Output

1. **Location**
   - Files are created in: `test_output/`
   - Format: `ETF_Analysis_YYYY-MM-DD_TICKERS.xlsx`

2. **Excel File Contents**
   - Price data tab
   - Dividend data tab
   - Calculated metrics tab

## Common Issues

1. **Missing Output Directory**
   - Create directory: `test_output/`
   - Or update path in `src/config.py`

2. **Package Import Errors**
   - Run: `pip install -r requirements.txt`
   - Check Python version: `python --version`

3. **Yahoo Finance Access**
   - Check internet connection
   - Verify ticker symbols exist

## Next Steps

1. Review [docs/DATA_FLOW.md](DATA_FLOW.md) for process details
2. Check [docs/CALCULATIONS.md](CALCULATIONS.md) for metrics info
3. See [docs/TESTING.md](TESTING.md) for validation steps
