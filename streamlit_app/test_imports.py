"""
Test script to verify imports and basic functionality
"""
import os
import sys

def test_imports():
    print("Testing imports...")
    
    # Add project root to path
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(root_dir)
    
    try:
        # Test streamlit import
        import streamlit as st
        print("[OK] Streamlit imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import streamlit: {e}")
        return False
        
    try:
        # Test plotly import
        import plotly.graph_objects as go
        print("[OK] Plotly imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import plotly: {e}")
        return False
    
    try:
        # Test local modules
        sys.path.append(os.path.join(root_dir, 'tests'))
        from test_etf_data_w_metrics import main as run_etf_analysis
        print("[OK] Test module imported successfully")
    except ImportError as e:
        print(f"[ERROR] Failed to import test module: {e}")
        return False
    
    print("\nChecking directories...")
    test_output_dir = os.path.join(root_dir, "Test Output")
    if os.path.exists(test_output_dir):
        print(f"[OK] Test Output directory exists: {test_output_dir}")
    else:
        print(f"[ERROR] Test Output directory not found: {test_output_dir}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\nAll tests passed! You can now run the Streamlit app.")
    else:
        print("\nSome tests failed. Please fix the issues before running the app.")
