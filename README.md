# ETF Analytics Dashboard 

## Overview
Python-based ETF analytics system for downloading data from Yahoo Finance, calculating performance metrics, with Excel output and Streamlit visualization.

## Quick Start
1. Create and activate virtual environment:
   ```bash
   python -m venv my_quant_env
   my_quant_env\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run dashboard:
   ```bash
   streamlit run streamlit_app/dashboard_xlsx_viewer.py
   ```

## Project Status 
- All core functionality working
- Environment: my_quant_env (required)
- Latest Backup: `S:\Dropbox\Scott Only Internal\Quant_Python_24\XLSX_Plot_Streamlit_Backup_121524b`
- Multi-ticker processing: Fully functional

## Documentation
See [Technical Documentation](./docs/TECHNICAL_GUIDE.md) for complete details.

### Core Features 
- Data Layer: Yahoo Finance integration, ETF management
- Model Layer: Performance metrics, Excel output
- Streamlit Layer: Dashboard visualization

## Project Structure
```
├── src/               # Source code
│   ├── data/         # Data handling
│   └── models/       # Core calculations
├── streamlit_app/    # Dashboard
├── tests/           # Test files
├── docs/            # Documentation
└── requirements.txt # Dependencies
```

## Support
1. Check [Technical Guide](./docs/TECHNICAL_GUIDE.md)
2. Review [Known Issues](./docs/troubleshooting/KNOWN_ISSUES.md)
3. Verify environment setup
4. Check latest backup
