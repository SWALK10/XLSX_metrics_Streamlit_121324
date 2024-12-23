# Project Structure

## Core Components

### Base Code (DO NOT MODIFY)
```
src/
├── data/
│   ├── stock_fetcher.py   # YFinance integration
│   ├── etf_manager.py     # ETF data management
│   └── excel_manager.py   # Excel operations
└── models/
    ├── performance_metrics.py  # Core calculations
    └── metrics_writer.py      # Excel output
```

### Streamlit Layer
```
streamlit_app/
├── components/
│   ├── ticker_input.py     # Ticker input handling
│   ├── metrics_display.py  # Metrics visualization
│   └── charts.py          # Future visualizations
├── utils/
│   ├── ticker_validator.py # Validation logic
│   └── excel_reader.py    # Excel data reading
└── dashboard_xlsx_viewer.py  # Main dashboard
```

## Documentation Structure
```
docs/
├── README.md              # Start here
├── structure/            # Project structure
├── ui/                   # UI documentation
├── history/             # Project history
└── troubleshooting/     # Known issues
```

## Search Terms
#structure #modules #components #organization
