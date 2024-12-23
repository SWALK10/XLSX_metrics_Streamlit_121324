"""
Unit tests for metrics calculations to ensure accuracy and consistency
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.models.performance_metrics import PerformanceMetrics
from src.models.metrics_writer import calculate_and_write_metrics

class TestMetricsCalculations(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        # Create sample price data
        dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='B')
        self.test_prices = pd.DataFrame({
            'SPY': 100 * (1 + np.random.normal(0.0001, 0.01, len(dates))).cumprod()
        }, index=dates)
        
        # Create sample dividend data
        div_dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='Q')
        self.test_dividends = pd.DataFrame({
            'SPY': [1.5] * len(div_dates)
        }, index=div_dates)
        
        self.perf = PerformanceMetrics()

    def test_return_calculations(self):
        """Test basic return calculations"""
        returns = self.perf.calculate_returns(self.test_prices['SPY'])
        
        # Verify return fields exist
        self.assertIn('daily_return', returns)
        self.assertIn('monthly_return', returns)
        self.assertIn('ytd_return', returns)
        
        # Verify return values are within reasonable bounds
        self.assertLess(abs(returns['daily_return']), 0.1)  # Daily return < 10%
        self.assertLess(abs(returns['monthly_return']), 0.3)  # Monthly return < 30%

    def test_risk_metrics(self):
        """Test risk metric calculations"""
        metrics = self.perf.calculate_risk_metrics(self.test_prices['SPY'])
        
        # Verify risk metric fields exist
        self.assertIn('volatility', metrics)
        self.assertIn('max_drawdown', metrics)
        self.assertIn('sharpe_ratio', metrics)
        
        # Verify metric values are within reasonable bounds
        self.assertGreater(metrics['volatility'], 0)
        self.assertLess(metrics['volatility'], 1)  # Volatility < 100%
        self.assertLess(metrics['max_drawdown'], 0)  # Drawdown should be negative
        self.assertGreater(metrics['max_drawdown'], -1)  # Drawdown > -100%

    def test_yield_calculation(self):
        """Test dividend yield calculation"""
        # Create a test Excel writer
        test_file = 'test_metrics.xlsx'
        with pd.ExcelWriter(test_file, engine='xlsxwriter') as writer:
            calculate_and_write_metrics(self.test_prices, self.test_dividends, writer)
        
        # Read back the metrics
        metrics_df = pd.read_excel(test_file, sheet_name='Metrics', index_col=0)
        
        # Verify yield calculation
        yield_value = metrics_df.loc['SPY', '%Yield']
        self.assertGreater(yield_value, 0)
        self.assertLess(yield_value, 0.1)  # Yield should be < 10%
        
        # Clean up
        os.remove(test_file)

    def test_calendar_year_returns(self):
        """Test calendar year return calculations"""
        # Create test data with known returns
        dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='B')
        prices = pd.DataFrame({
            'TEST': [100] * len(dates)
        }, index=dates)
        
        # Set specific start and end prices for 2022 and 2023
        prices.loc['2022-01-03', 'TEST'] = 100  # First trading day 2022
        prices.loc['2022-12-30', 'TEST'] = 90   # Last trading day 2022 (-10%)
        prices.loc['2023-01-03', 'TEST'] = 90   # First trading day 2023
        prices.loc['2023-12-29', 'TEST'] = 99   # Last trading day 2023 (+10%)
        
        # Calculate metrics
        with pd.ExcelWriter('test_calendar.xlsx', engine='xlsxwriter') as writer:
            calculate_and_write_metrics(prices, pd.DataFrame(), writer)
        
        # Read back the metrics
        metrics_df = pd.read_excel('test_calendar.xlsx', sheet_name='Metrics', index_col=0)
        
        # Verify calendar year returns
        self.assertAlmostEqual(metrics_df.loc['TEST', '2022%'], -0.10, places=2)
        self.assertAlmostEqual(metrics_df.loc['TEST', '2023%'], 0.10, places=2)
        
        # Clean up
        os.remove('test_calendar.xlsx')

if __name__ == '__main__':
    unittest.main()
