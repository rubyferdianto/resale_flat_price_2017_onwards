# Singapore Resale Flat Price Analysis Dashboard

## 📊 Project Overview

A comprehensive, production-ready Streamlit dashboard for analyzing Singapore's resale flat prices using official data from data.gov.sg. This interactive web application provides deep insights into housing market trends, geographic patterns, and statistical analysis with advanced data exploration capabilities.

## ✨ Key Features

### 🎯 Core Functionality
- **Real-time Data Integration**: Direct connection to Singapore's official data.gov.sg API
- **Performance Optimized**: Smart caching system with CSV storage (1.44x faster than direct API calls)
- **Comprehensive Dashboard**: 6 analysis sections with interactive visualizations
- **Advanced Data Explorer**: Multi-level sorting, pagination, and powerful filtering

### 📈 Analysis Sections
1. **Overview**: Dataset metrics, price statistics, and floor area analysis
2. **Price Trends**: Monthly trends, flat type comparisons, and distribution analysis
3. **Geographic Analysis**: Town-wise price analysis and transaction volumes
4. **Flat Analysis**: Price vs area/age correlations with scatter plots
5. **Market Insights**: YoY changes, market leaders, and recent trends
6. **Data Explorer**: Interactive filtering, sorting, and data export

### 🎨 User Experience
- **Professional UI**: Custom styling with optimized table layouts and red-themed headers
- **Smart Data Formatting**: Currency formatting, number alignment, and intuitive displays
- **Responsive Design**: Optimized for desktop viewing with proper column alignment
- **Export Functionality**: Download filtered data as CSV for further analysis

## 📋 Prerequisites

- Python 3.9 or higher
- Conda package manager (recommended) or pip
- Internet connection for API access
- 8GB+ RAM recommended for large dataset processing

## 🚀 Quick Start

### 1. Installation
```bash
# Clone or download the project
# Navigate to project directory

# Create and activate conda environment
conda env create -f environment.yml
conda activate resale-flat-analysis
```

### 2. Run the Dashboard
```bash
streamlit run streamlit_app.py
```

### 3. Access the Application
Open your browser and navigate to: `http://localhost:8501`

## 🎮 Dashboard Features

### 📊 Overview Section
- **Dataset Metrics**: Total transactions, average prices, data period
- **Price Statistics**: Min, max, mean, median, standard deviation
- **Floor Area Statistics**: Comprehensive area analysis with smart formatting
- **Professional Tables**: Custom HTML tables with optimized alignment and styling

### 📈 Data Explorer (Advanced Features)
- **Multi-level Sorting**: Default month descending + user-selected secondary column
- **Smart Pagination**: 50 records per page with intuitive navigation
- **Advanced Filtering**: 
  - Multi-select towns and flat types
  - Month range selection with recent-first ordering
  - Price range slider with formatted display
- **Data Export**: Download filtered results as CSV
- **Professional Formatting**: 
  - Right-aligned price columns with monospace font
  - Smart number formatting with currency symbols
  - Responsive table design

### 🗺️ Geographic & Market Analysis
- **Town Comparisons**: Top 15 towns by price and transaction volume
- **Price Trends**: Monthly trends by flat type with interactive charts
- **Market Insights**: YoY changes, market leaders, recent trends
- **Correlation Analysis**: Price vs area, age relationships

## 📁 Project Structure

```
resale_flat_price_2017_onwards/
├── streamlit_app.py         # Main dashboard application (726 lines)
├── data_fetcher.py          # API integration and caching system
├── environment.yml          # Conda environment configuration  
├── readme.md               # Project documentation
├── resale_flat_data.csv    # Cached dataset (auto-generated)
└── data_metadata.json      # Dataset metadata (auto-generated)
```

## 🔧 Technical Details

### Performance Optimization
- **Smart Caching**: Streamlit @st.cache_data with 1-hour TTL
- **CSV vs API**: Automated fallback system (CSV 1.44x faster)
- **Data Processing**: Efficient pandas operations with numpy integration
- **Memory Management**: Strategic sampling for large visualizations

### Data Processing Pipeline
1. **API Connection**: Automated pagination for complete dataset retrieval
2. **Data Cleaning**: Type conversion, date parsing, calculated fields
3. **Feature Engineering**: Price per sqm, flat age calculations
4. **Caching Strategy**: Local CSV storage with metadata tracking
```bash
export DATA_CACHE_DIR="./data"
export API_TIMEOUT=30
export CSV_UPDATE_INTERVAL="daily"
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

- **For First-Time Setup**: Run `python demo.py` to test basic connectivity
- **For Development**: Use `python run_analysis.py` to test data processing
- **For Production**: Use CSV caching and scheduled updates

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
- **726 lines** of production-ready Streamlit code
- **Modular Functions**: Separate functions for each analysis section
- **Custom HTML/CSS**: Precise control over table formatting and alignment
- **Error Handling**: Robust data validation and fallback mechanisms

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

## 🔄 Updates

- **v1.0.0**: Initial release with basic data fetching and Streamlit dashboard
- **v1.1.0**: Added performance comparison and CSV caching
- **v1.2.0**: Enhanced visualizations and predictive analytics
- **v1.3.0**: Added geographic analysis and advanced filtering
- **v1.4.0**: UI/UX improvements with right-aligned price columns and theme compatibility
- **v1.5.0**: Enhanced filtering with month selection and improved data formatting
- **v1.6.0**: Advanced UI improvements with red headers and enhanced price range display

### Latest Updates (v1.6.0)
- ✅ **Enhanced Data Explorer**: Custom HTML table with right-aligned price columns
- ✅ **Professional Formatting**: Currency formatting with S$ prefix and comma separators
- ✅ **Dark Theme Support**: Transparent backgrounds for better theme compatibility
- ✅ **Improved Readability**: Monospace font for price columns ensures consistent alignment
- ✅ **Cross-browser Compatibility**: Multiple CSS/JavaScript targeting methods for reliability
- ✅ **Month Filter**: Added month selection filter for time-based data analysis with reverse chronological order
- ✅ **Smart Number Display**: Floor area shows as integers when appropriate (85.0 → 85)
- ✅ **Enhanced Date Format**: Month column displays in readable Jan-2017 format
- ✅ **Red Column Headers**: Bold red headers for enhanced visual hierarchy and professional appearance
- ✅ **Enhanced Price Range Slider**: S$ formatting with real-time range display and comma separators

---

*Last updated: August 2025*


