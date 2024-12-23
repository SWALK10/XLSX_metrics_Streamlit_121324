# UI Documentation

## Quick Links
- [Layout Guide](./LAYOUT.md)
- [Styling Solutions](./STYLING.md)
- [Component Guide](./COMPONENTS.md)

## Overview
The Streamlit dashboard provides an interactive interface for viewing ETF metrics, matching Excel formatting exactly.

## Key Features
1. **Metrics Display**
   - Excel-matching formatting
   - Color coding (red/green for negative/positive)
   - Two-tab layout (Metrics and Correlation Analysis)

2. **Data Formatting**
   - Percentages: 1 decimal place (e.g., 1.2%)
   - Sharpe ratio: 2 decimal places
   - Shortened ETF names
   - Excel-exact formatting

3. **Interactive Elements**
   - Ticker input
   - Analysis button
   - Tab navigation

## Component Structure
```
streamlit_app/
├── components/
│   ├── ticker_input.py
│   ├── metrics_display.py
│   └── charts.py
└── utils/
    └── excel_reader.py
```

## Search Terms
#ui #streamlit #dashboard #layout #components
