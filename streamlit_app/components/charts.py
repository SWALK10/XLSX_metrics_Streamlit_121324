"""
Charts component for the Streamlit dashboard
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_price_history(excel_file: str):
    """
    Create an interactive price history chart
    """
    try:
        # Read price data
        df = pd.read_excel(excel_file, sheet_name='Daily Prices')
        df.set_index('Date', inplace=True)
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces for each ticker
        colors = ['blue', 'red', 'green', 'purple', 'orange']  # Add more if needed
        
        for idx, column in enumerate(df.columns):
            color = colors[idx % len(colors)]
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[column],
                    name=column,
                    line=dict(color=color)
                ),
                secondary_y=False
            )
        
        # Update layout
        fig.update_layout(
            title="Price History",
            xaxis_title="Date",
            yaxis_title="Price",
            height=600,
            hovermode='x unified',
            showlegend=True
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        return True
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return False
