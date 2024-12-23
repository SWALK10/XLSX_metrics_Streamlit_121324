import pandas as pd
import os
from datetime import datetime, date
import yfinance as yf

def test_na_handling():
    """Isolated test for NA handling in Excel"""
    # Test directory
    output_dir = "S:/Dropbox/Scott Only Internal/Quant_Python_24/XLSX_metrics_Streamlit_121324/Test Output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create sample data with gaps
    dates = pd.date_range(start='2020-01-01', end='2024-12-16', freq='B')
    data = {
        'ISPY': [100.0 if i % 5 != 0 else None for i in range(len(dates))],
        'SPY': [200.0 if i % 3 != 0 else None for i in range(len(dates))]
    }
    
    df = pd.DataFrame(data, index=dates)
    
    # Write to Excel with NA()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    excel_path = os.path.join(output_dir, f"na_test_{timestamp}.xlsx")
    
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Test_NA', na_rep='=NA()')
    
    print(f"Test file written to: {excel_path}")
    return excel_path

if __name__ == "__main__":
    test_na_handling()
