# Testing Instructions

## Overview
The project includes both unit tests and integration tests to ensure reliability and accuracy of calculations.

## Prerequisites
- Python 3.8 or higher
- Required packages installed (see requirements.txt)
- Write access to test_output directory

## Running Tests

### 1. Integration Tests
Tests the entire workflow from data download to Excel output.

```bash
# From the tests directory
python test_etf_metrics.py

# Expected output:
# - Console output showing download progress
# - Excel file created in test_output directory
# - Success message with file location
```

### 2. Unit Tests
Tests individual calculation components and functions.

```bash
# From the tests directory
python test_metrics_calculations.py

# Expected output:
# - Test results for each calculation
# - Any failures will show detailed error messages
```

## Validation Steps

### 1. Integration Test Validation
After running `test_etf_metrics.py`, verify:

1. **File Creation**
   - New Excel file created in test_output directory
   - Filename includes current date and tickers

2. **Data Completeness**
   - All sheets present (Daily Prices, Unadjusted Prices, Dividends, Metrics)
   - Data from 2020-01-01 to present
   - No missing values in key fields

3. **Metrics Sheet**
   - All tickers present (SPY, JNK, IEI)
   - Full names displayed correctly
   - All metrics populated
   - Proper formatting applied

### 2. Unit Test Validation
After running `test_metrics_calculations.py`, verify:

1. **Test Coverage**
   - Return calculations
   - Risk metrics
   - Yield calculations
   - Calendar year returns

2. **Error Cases**
   - Handling of missing data
   - Boundary conditions
   - Invalid inputs

## Common Issues and Solutions

### 1. File Access Errors
```
ERROR: Permission denied
Solution: Close any open Excel files and retry
```

### 2. Data Download Issues
```
ERROR: No data found for ticker
Solution: Check internet connection and retry
```

### 3. Calculation Errors
```
ERROR: Invalid calculation result
Solution: Check input data ranges and retry
```

## Adding New Tests

### 1. Unit Tests
Add new test methods to `test_metrics_calculations.py`:
```python
def test_new_metric(self):
    """Test description"""
    # Test setup
    # Test execution
    # Assertions
```

### 2. Integration Tests
Add new validation steps to `test_etf_metrics.py`:
```python
# Add new ticker
tickers = ['SPY', 'JNK', 'IEI', 'NEW_TICKER']

# Add new validation
print(f"New metric value: {metric_value}")
```
