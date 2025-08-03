# Singapore Resale Flat Price Analysis Dashboard

## 📊 Overview

An interactive Streamlit dashboard for analyzing Singapore resale flat prices using official data from data.gov.sg. Provides comprehensive insights into housing market trends, geographic patterns, and statistical analysis with intelligent data management.

## ✨ Key Features

- **Real-time Data**: Direct connection to Singapore's official data.gov.sg API
- **Smart Caching**: Performance-optimized with CSV storage (1.44x faster than API calls)
- **6 Analysis Sections**: Overview, Price Trends, Geographic Analysis, Flat Analysis, Market Insights, Data Explorer
- **Year Filtering**: Comprehensive temporal analysis across all sections (defaults to 2025)
- **Interactive Maps**: Geographic visualization with exact table record synchronization
- **Data Export**: Download filtered results as CSV
- **Smart Refresh**: Intelligent system prevents unnecessary API calls

## 🚀 Quick Start

### 1. Installation
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
# Using startup script (recommended)
./run_dashboard.sh

# OR manually
source .venv/bin/activate
streamlit run streamlit_app.py
```

### 3. Access
Open your browser: `http://localhost:8501`

## 🎮 Dashboard Sections

### 📊 Overview
- Dataset metrics and statistics
- Price and floor area analysis
- Year-based filtering

### 📈 Price Trends
- Monthly price trends
- Flat type comparisons
- Interactive charts

### 🗺️ Geographic Analysis
- Town-wise price analysis
- Transaction volume mapping
- Top performers by region

### 🏢 Flat Analysis
- Price vs floor area correlations
- Age impact analysis
- Scatter plot visualizations

### 💡 Market Insights
- Year-over-year changes
- Market leaders identification
- Recent trend analysis

### 🔍 Data Explorer
- Interactive filtering (town, flat type, month, price range)
- 15 records per page with pagination
- Interactive map showing exact table records
- Multi-level sorting options
- CSV export functionality

## 🗺️ Map Visualization

The Data Explorer includes an interactive map that displays exactly the same records shown in the table:
- **Synchronized Data**: Map shows the exact 15 records from the current table page
- **Dynamic Updates**: Changes with pagination, sorting, and filtering
- **Geographic Context**: OpenStreetMap with price-based color coding and size scaling
- **Rich Hover Information**: Detailed property information on hover

## �️ Technical Details

### Data Management
- **Source**: Singapore data.gov.sg API (212K+ records from 2017-2025)
- **Caching**: Local CSV storage with metadata tracking
- **Refresh Logic**: Month-based detection system
- **Performance**: Strategic sampling for large visualizations

### Project Structure
```
├── streamlit_app.py         # Main dashboard (1400+ lines)
├── data_fetcher.py          # API integration and caching
├── run_dashboard.sh         # Startup script
├── requirements.txt         # Dependencies
├── resale_flat_data.csv     # Cached dataset (auto-generated)
└── data_metadata.json      # Metadata (auto-generated)
```

## � Troubleshooting

### Common Issues

1. **"Failed to load data" Error**
   ```bash
   # Solution: Use startup script
   ./run_dashboard.sh
   
   # OR activate environment manually
   source .venv/bin/activate
   streamlit run streamlit_app.py
   ```

2. **Environment Issues**
   ```bash
   # For externally-managed-environment error
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Data Loading Issues**
   - Ensure environment is activated
   - Check internet connection
   - Delete CSV files to force fresh API fetch

## 📈 Data Source

- **API**: https://data.gov.sg/api/action/datastore_search
- **Dataset**: Singapore HDB Resale Flat Prices (2017 onwards)
- **Update Frequency**: Monthly
- **Records**: 212K+ transactions

## 🙏 Acknowledgments

- **Data.gov.sg**: Official Singapore government data portal
- **HDB Singapore**: Housing & Development Board
- **Streamlit Community**: Framework and documentation

---

**Built with ❤️ using Streamlit and Singapore's Open Data Initiative**

*Last updated: August 2025*

## 🚨 Troubleshooting

### "Failed to load data" Error

If you see this error, it's usually because the virtual environment isn't activated:

**Solution 1: Use the startup script**
```bash
./run_dashboard.sh
```

**Solution 2: Manual environment activation**
```bash
# For virtual environment users:
source .venv/bin/activate
streamlit run streamlit_app.py

# For conda users:
conda activate resale-flat-analysis
streamlit run streamlit_app.py
```

**Solution 3: Check data files**
```bash
# Verify CSV exists and has data
ls -la resale_flat_data.csv
head -5 resale_flat_data.csv
```

### Common Issues

1. **Environment Not Activated**
   ```
   Error: ModuleNotFoundError: No module named 'streamlit'
   ```
   - **Fix**: Always activate your environment before running Streamlit
   - **Quick Fix**: Use `./run_dashboard.sh`

2. **Virtual Environment Issues**
   ```
   error: externally-managed-environment
   ```
   - **Fix**: Use virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
   - **Then**: `pip install -r requirements.txt`

3. **Data Loading Issues**
   ```
   Failed to load data. Please check your internet connection and try again.
   ```
   - **Fix**: Ensure environment is activated and dependencies are installed
   - **Check**: Data files exist with `ls resale_flat_data.csv`
   - **Reset**: Delete CSV files to force fresh API fetch

## 🎮 Dashboard Features

### 📊 Overview Section
- **Dataset Metrics**: Total transactions, average prices, data period
- **Price Statistics**: Min, max, mean, median, standard deviation
- **Floor Area Statistics**: Comprehensive area analysis with smart formatting
- **Professional Tables**: Custom HTML tables with optimized alignment and styling

### 📈 Data Explorer (Advanced Features)
- **Complete Column Visibility**: All CSV columns available including block, street_name, storey_range, flat_model, lease_commence_date, remaining_lease
- **Multi-level Sorting**: Default month descending + user-selected secondary column
- **Smart Pagination**: 50 records per page with intuitive navigation
- **Year Filtering**: Comprehensive temporal analysis with default to 2025
- **Advanced Filtering**: 
  - Multi-select towns and flat types
  - Month range selection with recent-first ordering
  - Price range slider with formatted display
- **Data Export**: Download filtered results as CSV with intelligent filename generation
- **Professional Formatting**: 
  - Right-aligned price columns with monospace font
  - Smart number formatting with currency symbols
  - Custom HTML tables for precise control
  - Responsive table design optimized for all columns

### � Data Management Features
- **Smart Data Freshness**: Color-coded indicators showing data age
  - ✅ Green: Fresh data (today)
  - 📅 Blue: Recent data (1-7 days)
  - ⚠️ Orange: Aging data (8-30 days)
  - 🔴 Red: Old data (30+ days) - Refresh recommended
- **One-Click Refresh**: Manual data refresh with progress tracking
- **Safety Confirmations**: Warning dialogs before API calls
- **Progress Indicators**: Real-time status during data fetching
- **Auto-reload**: Automatic page refresh after successful data update

### �🗺️ Geographic & Market Analysis
- **Town Comparisons**: Top 15 towns by price and transaction volume
- **Price Trends**: Monthly trends by flat type with interactive charts
- **Market Insights**: YoY changes, market leaders, recent trends
- **Correlation Analysis**: Price vs area, age relationships

## 📁 Project Structure

```
resale_flat_price_2017_onwards/
├── streamlit_app.py         # Main dashboard application (1400+ lines)
├── data_fetcher.py          # API integration and caching system (227 lines)
├── run_dashboard.sh         # Easy startup script
├── environment.yml          # Conda environment configuration  
├── requirements.txt         # Pip requirements (preserved for compatibility)
├── readme.md               # Comprehensive project documentation
├── resale_flat_data.csv    # Cached dataset (auto-generated, 212K+ records)
├── data_metadata.json      # Dataset metadata (auto-generated)
└── .gitignore              # Git ignore rules
```

**Core Files (Essential):**
- `streamlit_app.py` - The main dashboard application with 6 analysis sections and intelligent data management
- `data_fetcher.py` - Handles API connections, data caching, and performance optimization
- `run_dashboard.sh` - Startup script for easy launching with environment activation

**Configuration Files:**
- `environment.yml` - Conda environment setup with all dependencies
- `requirements.txt` - Pip package requirements (maintained for pip users)

**Data Files (Auto-generated):**
- `resale_flat_data.csv` - Local data cache with complete dataset (212,808+ records from 2017-2025)
- `data_metadata.json` - Data freshness tracking for intelligent refresh management

## 🔧 Technical Details

### Performance & Data Management
- **Intelligent Caching**: Streamlit @st.cache_data with 1-hour TTL plus smart refresh logic
- **Hybrid Data Access**: CSV cache (1.44x faster) with API fallback and month-based refresh detection
- **Smart Refresh System**: Prevents unnecessary API calls when data is current for the month
- **Progress Tracking**: Real-time feedback during data operations with comprehensive error handling
- **Memory Management**: Strategic sampling for large visualizations (5000 records for scatter plots)
- **Complete Data Access**: All CSV columns exposed in Data Explorer for comprehensive analysis

### Data Processing Pipeline
1. **API Connection**: Automated pagination for complete dataset retrieval from data.gov.sg
2. **Data Cleaning**: Type conversion, date parsing, calculated fields (price_per_sqm, flat_age)
3. **Feature Engineering**: Advanced calculations and data enrichment
4. **Intelligent Caching**: Local CSV storage with metadata tracking and month-based freshness detection
5. **Year-based Analysis**: Comprehensive temporal filtering across all dashboard sections
```bash
export DATA_CACHE_DIR="./data"
export API_TIMEOUT=30
export REFRESH_CHECK_INTERVAL="monthly"
```

## 🚨 Troubleshooting

### Common Issues

1. **API Access Issues**
   ```
   Error: HTTP Error 403: Forbidden
   ```
   - The API may have rate limiting or access restrictions
   - Try running the script at different times
   - Consider using cached data if available

2. **Package Installation Issues**
   ```
   error: externally-managed-environment
   ```
   - Use virtual environment: `python3 -m venv venv && source venv/bin/activate`
   - Or use conda: `conda env create -f environment.yml`

3. **Memory Issues with Large Datasets**
   - Use data sampling in Streamlit: `df.sample(n=10000)`
   - Implement pagination for large data loads
   - Consider data filtering before analysis

4. **Streamlit Performance Issues**
   - Use `@st.cache_data` decorators (already implemented)
   - Reduce data size with filters
   - Use `st.spinner()` for better UX during loading

### Performance Tips

- **For First-Time Setup**: Use the startup script `./run_dashboard.sh` for automated environment setup
- **For Development**: Activate environment and run `streamlit run streamlit_app.py`
- **For Production**: Leverage intelligent refresh system and CSV caching for optimal performance
- **Data Management**: Use the smart refresh system that prevents unnecessary API calls when data is current

## 📈 Analysis Features

### Custom Styling & Responsiveness
- **Optimized Table Widths**: Statistics tables reduced to 70% width for better visual balance
- **Column Proportions**: 20% statistic names, 80% data values for optimal readability
- **Professional Spacing**: Enhanced padding and margins for clean presentation
- **Red Header Theme**: Consistent branding with #dc3545 color scheme

## 📊 Data Source

The project uses Singapore's official resale flat price data from:
- **API Endpoint**: https://data.gov.sg/api/action/datastore_search  
- **Dataset ID**: d_8b84c4ee58e3cfc0ece0d773c8ca6abc
- **Data Period**: 2017 onwards (212,808+ records)
- **Update Frequency**: Monthly
- **Fields**: Month, town, flat type, block, street, storey range, floor area, model, lease dates, resale price

## 🚀 Performance & Architecture

### Optimization Features
- **Smart Caching**: 1-hour TTL with automatic fallback
- **CSV vs API**: 1.44x performance improvement with local storage
- **Memory Efficiency**: Strategic sampling for large visualizations
- **Responsive UI**: Optimized for desktop analysis workflows

### Sorting & Navigation
- **Multi-level Sorting**: Month descending + user-selected secondary column
- **Intelligent Pagination**: 50 records per page with intuitive controls
- **Advanced Filtering**: Real-time multi-dimensional data filtering
- **Export Functionality**: CSV download with formatting preservation

## 🛠️ Development Notes

### Code Quality
- **1400+ lines** of production-ready Streamlit code (main dashboard)
- **227 lines** of data fetching and caching logic  
- **1,627+ total lines** of clean, documented Python code
- **Modular Architecture**: Separate functions for each analysis section with consistent year filtering
- **Custom HTML/CSS**: Precise control over table formatting, alignment, and professional styling
- **Intelligent Systems**: Smart refresh logic with month-based detection and user education
- **Error Handling**: Robust data validation, fallback mechanisms, and comprehensive user feedback
- **Complete Feature Coverage**: All CSV columns exposed, comprehensive year filtering, advanced sorting

### Dependencies
```yaml
# environment.yml
dependencies:
  - python=3.9
  - streamlit>=1.25
  - pandas>=1.5
  - numpy>=1.24
  - plotly>=5.0
  - requests>=2.28
```

## 🙏 Acknowledgments

- **Data.gov.sg**: Official Singapore government data portal
- **HDB Singapore**: Housing & Development Board for data collection
- **Streamlit Community**: Excellent framework and documentation

---

**Last Updated**: August 2025 | **Version**: 2.0.0 Production Ready

## 🎨 UI/UX Enhancements

### Price Column Formatting & Alignment

The Data Explorer section includes several UI improvements for better data readability:

#### 📊 **Enhanced Data Display**
- **Currency Formatting**: All price columns display with "S$" prefix and comma separators (e.g., "S$650,000")
- **Right Alignment**: Price columns ("Resale Price" and "Price per sqm") and Floor Area column are right-aligned for better numerical comparison
- **Monospace Font**: Price and numerical values use monospace font family for consistent digit alignment
- **Smart Number Formatting**: Floor area displays as integers when appropriate (85.0 → 85) and preserves decimals when needed (85.5 → 85.5)
- **Date Formatting**: Month column displays in readable format (Jan-2017, Feb-2017, etc.)
- **Red Column Headers**: Bold red column headers for enhanced visual hierarchy and professional appearance
- **Theme Compatibility**: Table backgrounds are transparent to work with both light and dark themes

#### 🔧 **Technical Implementation**
- **Custom HTML Table**: Uses custom HTML table generation for precise styling control
- **CSS & JavaScript Integration**: Multiple targeting methods ensure alignment works across different browsers
- **Responsive Design**: Table adapts to container width while maintaining alignment
- **Cross-browser Compatibility**: Enhanced selectors for different Streamlit versions

#### 📋 **Data Explorer Features**
- **Interactive Filters**: Multi-select dropdowns for towns, flat types, and months with intuitive date formatting
- **Enhanced Month Filter**: Months displayed in reverse chronological order (newest first) for better usability
- **Price Range Slider**: Dynamic price range filtering with S$ formatting and comma-separated value display
- **Real-time Range Display**: Caption showing selected price range with proper currency formatting
- **Advanced Filtering**: Combined filtering across multiple dimensions (location, property type, time period, price)
- **Sample Data Display**: Shows first 100 records with professional formatting and red column headers
- **CSV Export**: Download filtered data with proper formatting maintained

### Code Location
The alignment improvements are implemented in the `create_data_explorer()` function:
- **Lines 421-445**: Custom HTML table generation with right-aligned price columns
- **Enhanced styling**: Transparent backgrounds for dark theme compatibility
- **Multiple fallback methods**: Ensures alignment works reliably across different environments

## 🚀 Performance Optimization

### Recommendations Based on Use Case:

- **For Data Scientists/Analysts**: Use CSV caching for faster repeated analysis
- **For Real-time Applications**: Use direct API calls for latest data
- **For Large-scale Analysis**: Implement incremental updates with CSV storage
- **For Demonstrations**: Use sample data with API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For questions or support, please contact:
- Email: your.email@example.com
- GitHub: [Your GitHub Profile](https://github.com/rubyferdianto)

## 🙏 Acknowledgments

- Data.gov.sg for providing open access to resale flat price data
- Singapore Housing & Development Board (HDB) for data collection
- Streamlit community for excellent documentation and examples

## 📊 Data Notes

1. **Floor Area**: Includes recess area purchased, space adding items under HDB's upgrading programmes, roof terrace, etc.
2. **Transaction Exclusions**: Excludes resale transactions that may not reflect full market price (e.g., resale between relatives, part shares)
3. **Price Indication**: Resale prices are indicative only as agreed prices depend on many factors
4. **Data Accuracy**: Data is sourced from official HDB records and updated monthly

## 🔄 Smart Data Refresh System

### How the Intelligent Refresh Works:

1. **Automatic Detection**: System calculates months behind using current date vs. latest data month
2. **Smart UI Display**: 
   - **Data Behind**: Shows "🔄 Data Update Available" with full refresh capability
   - **Data Current**: Shows "🔄 Data Management" with educational warnings
3. **User Education**: Clear messaging about HDB monthly update cycles and optimal refresh timing
4. **Resource Efficiency**: Prevents unnecessary API calls when data is already current

### Refresh Process:
1. **Check Data Status**: Look at the sidebar data management section
2. **Smart Button Logic**: 
   - Enabled with update messaging when data is behind
   - Enabled with warning when data is current (educational purpose)
3. **Confirm Action**: Review the intelligent warning and click "✅ Continue" or "🚫 Understood"
4. **Monitor Progress**: Real-time progress indicators with comprehensive error handling
5. **Auto-reload**: Automatic page refresh after successful data update

### Safety Features:
- Month-based freshness detection with sophisticated calculation logic
- Educational warnings about HDB data release cycles
- Progress tracking during refresh with detailed status messages
- Comprehensive error handling with user-friendly feedback
- Automatic cache clearing and page reload after successful update
- Resource-efficient design preventing unnecessary API calls

## 🎯 Use Cases

- **Real Estate Analysis**: Market trends and pricing insights
- **Investment Research**: Geographic and temporal price patterns  
- **Academic Research**: Housing market data analysis
- **Government Planning**: Policy impact assessment
- **Business Intelligence**: Market positioning and strategy

## 🚀 Future Enhancements

- [ ] Machine learning price predictions
- [ ] Mobile-responsive design
- [ ] Real-time data streaming
- [ ] Advanced statistical models
- [ ] Export to multiple formats (Excel, PDF)
- [ ] User authentication and saved filters

## 📞 Support & Contact

- **GitHub**: [rubyferdianto/resale_flat_price_2017_onwards](https://github.com/rubyferdianto)
- **Documentation**: Comprehensive inline code documentation
- **Issues**: GitHub Issues for bug reports and feature requests

## 🙏 Acknowledgments

- **Data.gov.sg**: Official Singapore government data portal
- **HDB Singapore**: Housing & Development Board for data collection
- **Streamlit Community**: Excellent framework and documentation

## 📊 Data Notes

1. **Floor Area**: Includes recess area purchased, space adding items under HDB's upgrading programmes, roof terrace, etc.
2. **Transaction Exclusions**: Excludes resale transactions that may not reflect full market price (e.g., resale between relatives, part shares)
3. **Price Indication**: Resale prices are indicative only as agreed prices depend on many factors
4. **Data Accuracy**: Data is sourced from official HDB records and updated monthly

## 🔄 Version History

### Latest Updates (v2.1.0) - Data Refresh Feature
- ✅ **Smart Data Refresh**: One-click refresh with safety confirmations
- ✅ **Data Freshness Indicators**: Color-coded age indicators with recommendations
- ✅ **Progress Tracking**: Real-time feedback during API operations
- ✅ **Error Handling**: Robust error messages and recovery options
- ✅ **Auto-reload**: Automatic page refresh after successful updates
- ✅ **User Experience**: Intuitive warnings and confirmations before API calls

### Previous Updates (v2.0.0) - Production Ready
- ✅ **Enhanced Data Explorer**: Custom HTML table with right-aligned price columns
- ✅ **Professional Formatting**: Currency formatting with S$ prefix and comma separators
- ✅ **Dark Theme Support**: Transparent backgrounds for better theme compatibility
- ✅ **Improved Readability**: Monospace font for price columns ensures consistent alignment
- ✅ **Cross-browser Compatibility**: Multiple CSS/JavaScript targeting methods for reliability
- ✅ **Optimized Performance**: Streamlined dependencies and code cleanup
- ✅ **Documentation**: Comprehensive README with technical details

---

**Built with ❤️ using Streamlit and Singapore's Open Data Initiative**

*Last updated: August 2025*


