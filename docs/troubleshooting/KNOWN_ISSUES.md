# Known Issues & Solutions

## UI Issues

### Logo Display
1. **Issue**: Logo sizing inconsistency
   - **Solution**: Use direct width control (width=150) in st.image()
   - **Status**: ✅ Resolved

2. **Issue**: Logo positioning
   - **Solution**: Three-column layout [1,2,1]
   - **Status**: ✅ Resolved

### Table Styling
1. **Issue**: Header alignment
   - **Solution**: Custom CSS for numeric columns
   - **Status**: 🔄 Partial (working on better solution)

2. **Issue**: Font weight control
   - **Solution**: Pending Streamlit CSS support
   - **Status**: ⏳ Waiting

## Data Issues

### Yahoo Finance
1. **Issue**: Rate limiting
   - **Solution**: Implement caching
   - **Status**: ✅ Resolved

2. **Issue**: Missing data handling
   - **Solution**: Fallback to previous valid data
   - **Status**: ✅ Resolved

## Environment Issues

### Virtual Environment
1. **Issue**: Package conflicts
   - **Solution**: Use my_quant_env
   - **Status**: ✅ Resolved

2. **Issue**: Path resolution
   - **Solution**: Use absolute paths
   - **Status**: ✅ Resolved

## Failed Solutions Log

### Logo Styling
- ❌ CSS containers with width settings
- ❌ use_column_width parameter
- ❌ Small width values (45-67px)
- ❌ CSS with !important tags
- ❌ Outside column placement

### Table Styling
- ❌ Direct CSS injection
- ❌ Custom HTML rendering
- ❌ DataFrame style API

## Search Terms
#issues #troubleshooting #solutions #bugs
