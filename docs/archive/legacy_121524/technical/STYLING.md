# UI Styling Guide

## Logo Implementation

### Working Solution ✅
1. **Layout Structure**
   - Three-column layout [1,2,1]
   - Logo in right column
   - Direct width control

2. **Image Settings**
   ```python
   st.image(logo_path, width=150)
   ```

3. **Key Points**
   - No CSS containers needed
   - Clean, predictable scaling
   - Original image (1390x1090) works without pre-processing

### Failed Approaches ❌
1. **CSS Containers**
   - Issue: Unpredictable scaling
   - Attempted: Width settings in containers

2. **Column Width Parameter**
   ```python
   st.image(logo_path, use_column_width=True)
   ```
   - Issue: Insufficient control
   - Result: Inconsistent sizing

3. **Small Width Values**
   ```python
   st.image(logo_path, width=45)
   ```
   - Issue: Too small
   - Range tested: 45-67px

4. **CSS with !important**
   ```css
   .stImage { width: 150px !important; }
   ```
   - Issue: Doesn't override effectively
   - Result: Inconsistent behavior

5. **Outside Column Structure**
   - Issue: Breaks layout
   - Impact: Affects entire dashboard structure

## Table Styling

### Working Solution ✅
1. **Column Headers**
   - Center-aligned numeric columns
   - Left-aligned text columns
   - Consistent font size

2. **Data Cells**
   - Color coding: red/green for negative/positive
   - Percentage formatting: 1 decimal place
   - Sharpe ratio: 2 decimal places

### Future Considerations
1. **Logo**
   - May need width adjustment if layout changes
   - Consider margin-top for vertical positioning
   - Monitor Streamlit image handling updates

2. **Table**
   - Potential for custom CSS when Streamlit adds support
   - Consider conditional formatting options
   - Plan for responsive design improvements

## Search Terms
#styling #logo #table #layout #streamlit
