import pandas as pd
import os
from datetime import datetime
from pandas.tseries.offsets import BDay

def test_market_na():
    """Test NA handling with realistic market data"""
    output_dir = "S:/Dropbox/Scott Only Internal/Quant_Python_24/XLSX_metrics_Streamlit_121324/Test Output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create business days only (market days)
    dates = pd.bdate_range(start='2020-01-01', end='2020-02-01', freq='B')
    dates = dates.date  # Convert to date objects, removing time component
    
    # Create sample data with realistic gaps
    # ISPY started trading later, so it should have NAs at the start
    ispy_data = [None] * 5 + [100.0] * (len(dates) - 5)  # First week is NA
    spy_data = [200.0] * len(dates)  # SPY has full history
    
    # Create DataFrame
    df = pd.DataFrame({
        'ISPY': ispy_data,
        'SPY': spy_data
    }, index=dates)
    
    # Write to Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    excel_path = os.path.join(output_dir, f"market_na_test_{timestamp}.xlsx")
    
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Test_NA')
        
        # Write dates and data manually to ensure proper formatting
        # Write headers
        worksheet.write(0, 0, 'Date')
        worksheet.write(0, 1, 'ISPY')
        worksheet.write(0, 2, 'SPY')
        
        # Write data
        for i, date in enumerate(dates, 1):
            worksheet.write(i, 0, date.strftime('%Y-%m-%d'))
            
            # Write ISPY data
            if ispy_data[i-1] is None:
                worksheet.write_formula(i, 1, '=NA()')
            else:
                worksheet.write(i, 1, ispy_data[i-1])
                
            # Write SPY data
            worksheet.write(i, 2, spy_data[i-1])
    
    print(f"Test file written to: {excel_path}")
    return excel_path

if __name__ == "__main__":
    test_market_na()
