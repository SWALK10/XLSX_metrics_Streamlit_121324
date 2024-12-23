"""
Relative Strength Chart Module

Creates relative performance charts comparing multiple tickers
with base 100 indexing from start date.

Uses adjusted close prices from 'Daily Prices' sheet of the dashboard Excel output.

=== WORKING ONLY - Change With Permission ===
Core functionality verified and tested. Any modifications require explicit approval.
=== END WORKING SECTION ===
"""

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

class RelativeStrengthChart:
    """
    Creates and manages relative strength charts using adjusted close prices
    """
    
    def __init__(self):
        """Initialize chart settings"""
        # === WORKING ONLY - Change With Permission ===
        self.default_window = '3Y'
        self.min_window = '3M'
        self.chart_height = 600
        self.chart_width = 1000
        # === END WORKING SECTION ===
        
    def create_chart(self, excel_path: str) -> go.Figure:
        """
        Creates relative strength chart from Excel data using adjusted close prices
        Args:
            excel_path: Path to Excel file containing 'Daily Prices' sheet
        Returns:
            Plotly figure object
        """
        try:
            # === WORKING ONLY - Change With Permission ===
            # Data loading and processing
            df = pd.read_excel(excel_path, sheet_name='Daily Prices')
            df.set_index('Unnamed: 0', inplace=True)
            df.index.name = 'Date'
            df.index = pd.to_datetime(df.index)
            
            # Get date range (3 years by default)
            end_date = df.index.max()
            start_date = end_date - pd.DateOffset(years=3)
            
            # Filter data and calculate relative strength
            df = df[df.index >= start_date]
            base_date = df.index[0]
            rel_strength = self._calculate_relative_strength(df, base_date)
            # === END WORKING SECTION ===
            
            # Create figure with subplots
            fig = go.Figure()
            
            # Add traces for each ticker
            for ticker in rel_strength.columns:
                fig.add_trace(
                    go.Scatter(
                        x=rel_strength.index,
                        y=rel_strength[ticker],
                        name=ticker,
                        mode='lines',
                        line=dict(width=2)
                    )
                )
            
            # Update layout
            fig.update_layout(
                title={
                    'text': '<span style="font-size: 24px">Relative Performance</span><br><span style="font-size: 14px">Adjusted Close (Base 100)</span>',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                },
                height=self.chart_height,
                width=self.chart_width,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                yaxis=dict(
                    title="Relative Performance (%)",
                    gridcolor='lightgrey',
                    showgrid=True,
                    zeroline=True,
                    zerolinecolor='grey'
                ),
                xaxis=dict(
                    title="Date",
                    gridcolor='lightgrey',
                    showgrid=True,
                    dtick="M3",  # Quarterly ticks
                    tickformat="%b\n%Y",  # Format: Month Year
                    tickmode="auto",
                    tickangle=0,
                    nticks=12  # Limit number of ticks
                ),
                # Add range selector buttons
                xaxis_rangeslider_visible=False,
                xaxis_rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3M", step="month", stepmode="backward"),
                        dict(count=6, label="6M", step="month", stepmode="backward"),
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(count=3, label="3Y", step="year", stepmode="backward"),
                        dict(step="all", label="Max")
                    ]),
                    y=1.1
                )
            )
            
            # Update hover template
            for trace in fig.data:
                trace.hovertemplate = "%{y:.1f}%<extra></extra>"
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating relative strength chart: {str(e)}")
            return None
    
    # === WORKING ONLY - Change With Permission ===
    def _calculate_relative_strength(self, price_data: pd.DataFrame, base_date: datetime) -> pd.DataFrame:
        """
        Calculate relative strength indexed to 100 at start date
        Args:
            price_data: DataFrame of adjusted close prices
            base_date: Date to index from
        Returns:
            DataFrame of relative strength values
        """
        try:
            # Get base prices
            base_prices = price_data.loc[base_date]
            
            # Calculate relative performance
            rel_strength = price_data.div(base_prices) * 100
            
            return rel_strength
            
        except Exception as e:
            logger.error(f"Error calculating relative strength: {str(e)}")
            return pd.DataFrame()
    # === END WORKING SECTION ===
