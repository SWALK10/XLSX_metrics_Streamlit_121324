# Dynamic Risk-Free Rate Implementation Changelog

## 2024-12-15: Implementation of Dynamic Risk-Free Rates and Sharpe Ratio Fix

### Changes Made
1. **Risk-Free Rate Source**
   - Using ^IRX (13-week Treasury Bill) data from Yahoo Finance
   - Historical rates are fetched for the entire calculation period
   - Rates range observed: 4.163% to 5.348%

2. **Sharpe Ratio Calculation Updates**
   - Modified to use daily-aligned historical rates instead of fixed rate
   - Fixed incorrect Sharpe ratio calculations that were showing extreme values
   - Example fix: SHV Sharpe corrected from -2.32 to -0.13, more accurately reflecting its nature as a short-term Treasury ETF
   - Added proper error handling and rate alignment

3. **Testing Results**
   - Verified correct Sharpe calculations across all ETFs
   - Confirmed proper alignment of Treasury rates with ETF returns
   - Example calculations:
     * SHV: -0.13 (corrected from -2.32)
     * SPY: 1.57
     * TLT: -0.53
   - All values now properly reflect risk-adjusted returns

### Technical Implementation Details
1. **Data Fetching**
   - Extended data fetch window by 30 days to ensure data availability
   - Implemented forward-fill and backward-fill for missing values
   - Aligned Treasury rates with ETF return dates

2. **Rate Processing**
   - Annual rates converted to daily rates (rate/252)
   - Rates stored as decimals (e.g., 0.04223 for 4.223%)
   - Proper date alignment between rates and returns

3. **Calculation Verification**
   - Daily return components properly scaled
   - Excess returns calculated with aligned risk-free rates
   - Standard deviation calculation verified
   - Annualization factor (√252) correctly applied

### Verification Steps
1. Treasury rate alignment with ETF dates
2. Proper handling of missing data points
3. Accurate daily rate conversions
4. Verified Sharpe calculations against manual checks

### Next Steps
1. Monitor performance impact of using historical rates
2. Consider implementing rolling window calculations
3. Add additional error handling for data availability

### Bug Fixes
1. **Critical Fix**: Corrected Sharpe ratio calculations that were showing extreme negative values
   - Root cause: Previous implementation had scaling issues
   - Impact: Most visible in low-volatility instruments like SHV
   - Resolution: Implemented proper scaling and verification in calculation pipeline
