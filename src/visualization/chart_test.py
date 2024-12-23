"""
Test script for relative strength chart using dashboard data
"""
import sys
from pathlib import Path
import pandas as pd
from relative_strength_chart import RelativeStrengthChart

def main():
    # Use existing dashboard data file
    test_file = "S:/Dropbox/Scott Only Internal/Quant_Python_24/XLSX_metrics_Streamlit_121324/Test Output/dashboard_data_20241215_1414_HYG_JNK_BKLN.xlsx"
    
    # First, let's examine the data
    df = pd.read_excel(test_file, sheet_name='Daily Prices')
    print("\nRaw data structure:")
    print(df.head())
    
    # Create and display chart
    print("\nCreating chart...")
    rs_chart = RelativeStrengthChart()
    fig = rs_chart.create_chart(test_file)
    
    if fig:
        print("Successfully created relative strength chart")
        fig.show()
    else:
        print("Failed to create chart")

if __name__ == '__main__':
    main()
