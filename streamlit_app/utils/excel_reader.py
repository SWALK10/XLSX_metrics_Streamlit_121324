"""
Utility functions for reading Excel files
"""
import os
import pandas as pd
from typing import Optional, Tuple
from datetime import datetime

def get_latest_excel(output_dir: str) -> Optional[str]:
    """
    Get the path to the latest Excel file in the output directory
    """
    try:
        files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
        if not files:
            return None
            
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
        return os.path.join(output_dir, latest_file)
    except Exception as e:
        print(f"Error finding latest Excel file: {str(e)}")
        return None

def get_file_info(file_path: str) -> Tuple[str, datetime]:
    """
    Get information about the Excel file
    """
    try:
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        file_name = os.path.basename(file_path)
        return file_name, creation_time
    except Exception as e:
        print(f"Error getting file info: {str(e)}")
        return "Unknown", datetime.now()
