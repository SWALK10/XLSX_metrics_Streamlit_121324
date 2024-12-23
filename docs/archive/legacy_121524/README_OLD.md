# ETF Analytics Dashboard Documentation

## 🎯 Project State At A Glance
- **Last Major Update**: 2024-12-14
- **Current Focus**: Streamlit Dashboard Enhancement
- **Active Features**: ETF Metrics, Excel Output, Dashboard
- **In Progress**: Ticker Input Integration
- **Up Next**: [See Roadmap](#roadmap)

## Critical Guideline
It is critical to only review and then suggest changes, but not to make any changes without first
- showing which existing modules would change and how
- receiving permission to change prior to making changes to existing code

## 📚 Documentation Structure
```
docs/
├── README.md               # This file - Start here + Setup
├── technical/             # Core technical docs + UI
│   ├── CALCULATIONS.md    # 🟢 Metric calculation rules
│   ├── DATA_FLOW.md      # 🟢 Data pipeline
│   ├── TESTING.md        # 🟢 Test procedures
│   └── ui/              # UI-related docs
├── development/          # Development guides
│   └── GIT_SETUP.md     # 🟢 Git procedures
├── state/               # Project state
│   ├── WORKING_STATE.md # 🟢 Current state
│   └── CHANGELOG.md     # 🟢 History
├── archive/            # Obsolete docs
└── review/            # Docs being reviewed
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git (optional, for version control)
- Access to Yahoo Finance (internet connection)

### Quick Setup
```bash
# 1. Create virtual environment
python -m venv my_quant_env

# 2. Activate environment (Windows)
my_quant_env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit dashboard
cd streamlit_app
streamlit run dashboard_xlsx_viewer.py
```

### Configuration
1. Output directory is set to:
   ```
   S:/Dropbox/Scott Only Internal/Quant_Python_24/Basic_XLSX_PlusCalc_Restored_120424/test_output
   ```
2. Verify this path exists or update in `src/config.py`

## 🔍 Documentation Guide

### Core Documentation (🟢)
1. [Technical Documentation](./technical/README.md)
   - [Calculations](./technical/CALCULATIONS.md)
   - [Data Flow](./technical/DATA_FLOW.md)
   - [Testing](./technical/TESTING.md)
   - [UI Styling](./technical/STYLING.md)

2. [Development](./development/README.md)
   - [Git Setup](./development/GIT_SETUP.md)

3. [Project State](./state/README.md)
   - [Working State](./state/WORKING_STATE.md)
   - [Change History](./state/CHANGELOG.md)

### Under Review (🟡)
- [Project Structure](./review/PROJECT_STRUCTURE.md)
- [Quick Start](./review/QUICK_START.md)

### Archived (🔴)
See [Archive](./archive/README.md) for obsolete documentation

## 🔍 Quick Access
### Current Documentation (🟢)
1. [Technical Documentation](./technical/README.md)
   - [Calculations](./technical/CALCULATIONS.md)
   - [Data Flow](./technical/DATA_FLOW.md)
   - [Testing](./technical/TESTING.md)
2. [Development](./development/README.md)
   - [Git Setup](./development/GIT_SETUP.md)
3. [Project State](./state/README.md)
   - [Working State](./state/WORKING_STATE.md)

### Under Review (🟡)
- [Project Structure](./review/PROJECT_STRUCTURE.md)
- [Quick Start](./review/QUICK_START.md)

### Archived (🔴)
See [Archive](./archive/README.md) for obsolete documentation

## 🗺️ Development Roadmap
### Current Sprint (Dec 2024)
1. **Dashboard Enhancement**
   - ✅ Add ticker input
   - ✅ Implement table styling
   - 🔄 Correlation heatmap
   - ⏳ Enhanced metrics display

### Upcoming Features
1. **Data Enhancement**
   - Additional metrics calculation
   - Historical trend analysis
   - Custom date ranges

2. **UI Improvements**
   - Advanced filtering
   - Custom metric grouping
   - Export functionality

## 🔄 Change Management
### Adding New Features
1. **Documentation First**
   - Create feature spec in `docs/specs/`
   - Update roadmap
   - Add to relevant documentation sections

2. **Implementation**
   - Follow existing patterns
   - Update documentation in parallel
   - Cross-reference all changes

3. **Review & Integration**
   - Update main README
   - Add to changelog
   - Document any known issues

### Documentation Rules
1. **Every Change Must**:
   - Be documented in changelog
   - Have clear status (🟢 🟡 🔴)
   - Include search keywords
   - Cross-reference related docs

2. **No Orphaned Information**:
   - All docs must be linked from README
   - Old docs marked as legacy
   - Migration plans for all legacy docs

## 🎯 Quick Reference Cards
### New Feature Checklist
```
📝 1. Documentation
   ☐ Feature spec created
   ☐ Roadmap updated
   ☐ Related docs identified

🛠️ 2. Implementation
   ☐ Follow existing patterns
   ☐ Update docs in parallel
   ☐ Add tests

📋 3. Integration
   ☐ Update README
   ☐ Add to changelog
   ☐ Document issues
```

### Documentation Checklist
```
📚 1. Structure
   ☐ Listed in inventory
   ☐ Clear status
   ☐ Proper location

🔍 2. Discoverability
   ☐ Search keywords
   ☐ Cross-references
   ☐ Clear purpose

📅 3. Maintenance
   ☐ Last updated date
   ☐ Migration plan (if legacy)
   ☐ Next review date
```

## Quick Links
### Essential Reading Order 
1. [Getting Started](./getting_started/SETUP.md) - Setup & Installation
2. [UI Documentation](./ui/README.md) - Dashboard Usage
3. [Known Issues](./troubleshooting/KNOWN_ISSUES.md) - Common Problems

### Development Resources 
1. [Project Structure](./structure/PROJECT_STRUCTURE.md) - Codebase Organization
2. [Calculations](./CALCULATIONS.md) - Core Metrics Rules
3. [Data Flow](./DATA_FLOW.md) - Pipeline Documentation

### Legacy Resources 
These files contain valuable information but are being reorganized:
- [Working State](./WORKING_STATE.md) - Current Known State
- [Testing Guide](./TESTING.md) - Test Procedures
- [Git Setup](./GIT_SETUP.md) - Version Control

## Project Overview
Python-based ETF analytics system with:
1. Data collection from Yahoo Finance
2. Performance metrics calculation
3. Excel output generation
4. Streamlit dashboard visualization

## Directory Structure
```
docs/
├── README.md               # This file - Start here
├── structure/             # Project structure documentation
├── ui/                    # UI-related documentation
├── history/              # Project history and changes
└── troubleshooting/      # Known issues and solutions
```

## Documentation Map

### For New Users
1. Start here (README.md)
2. Read [Getting Started](./getting_started/SETUP.md)
3. Review [User Guide](./user_guide/USAGE.md)

### For Developers
1. [Project Structure](./structure/PROJECT_STRUCTURE.md)
2. [Development Guide](./development/CONTRIBUTING.md)
3. [Testing Guide](./testing/README.md)

### For Maintenance
1. [Known Issues](./troubleshooting/KNOWN_ISSUES.md)
2. [Working State](./state/WORKING_STATE.md)
3. [Backup Procedures](./maintenance/BACKUP.md)

## Search Keywords
Each documentation section is tagged for easy searching:

### Core Documentation
- Project Structure: #structure #modules #components
- Getting Started: #setup #installation #configuration
- User Guide: #usage #examples #workflow

### Technical Documentation
- Development: #development #coding #guidelines
- Testing: #testing #validation #verification
- Maintenance: #maintenance #backup #recovery

### Feature Documentation
- UI: #streamlit #dashboard #layout
- Data: #yahoo #finance #metrics
- Output: #excel #formatting #calculations

## Recent Updates
- 12/14/24: Unified documentation structure
- 12/14/24: Added UI documentation
- 12/13/24: Added Streamlit dashboard
- 12/04/24: Initial project restoration

## Quick Start
See [Getting Started](./getting_started/SETUP.md) for detailed setup instructions.

```bash
# 1. Create virtual environment
python -m venv my_quant_env

# 2. Activate environment
my_quant_env\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit dashboard
streamlit run streamlit_app/dashboard_xlsx_viewer.py
```

## Documentation Status Report (2024-12-14)
### Documentation Status
```
docs/
├── CALCULATIONS.md        # 🟢 CURRENT: Core calculation rules
├── DATA_FLOW.md          # 🟢 CURRENT: Data pipeline documentation
├── DOCUMENTATION_MAP.md  # 🔴 OBSOLETE: Replaced by this README
├── GIT_SETUP.md         # 🟡 REVIEW: May need updates
├── PROJECT_STRUCTURE.md  # 🟡 REVIEW: Compare with new structure
├── QUICK_START.md       # 🟡 REVIEW: Compare with getting_started/
├── TESTING.md           # 🟢 CURRENT: Test procedures
└── WORKING_STATE.md     # 🟢 CURRENT: Project state
```

### Migration Plan
1. **Current Files** (🟢)
   - Move to appropriate directories
   - Maintain content
   - Update cross-references

2. **Review Needed** (🟡)
   - Compare with new documentation
   - Update if needed
   - Then move to new structure

3. **Obsolete** (🔴)
   - Archive or delete
   - Update references to new locations
