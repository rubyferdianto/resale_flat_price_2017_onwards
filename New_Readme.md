# Singapore Resale Flat Price Analysis Project

## 📊 Project Overview

This project provides a comprehensive analysis of Singapore's resale flat prices using data from data.gov.sg. The application includes data fetching, performance optimization, and interactive visualizations through Streamlit.

## 🚀 Features

- **Data Fetching**: Connect to Singapore's open data API to retrieve resale flat price data
- **Performance Optimization**: Compare CSV storage vs direct API calls for optimal performance
- **Interactive Dashboard**: Streamlit-powered web application for data exploration
- **Comprehensive Analysis**: Statistical analysis, trend visualization, and price predictions
- **Data Export**: Save processed data in multiple formats

## 📋 Prerequisites

- Python 3.9 or higher
- Conda package manager
- Internet connection for API access

## 🛠️ Installation

### Option 1: Automated Setup (Recommended)
```bash
python3 setup.py
```
This script will guide you through the installation process.

### Option 2: Manual Setup

#### Using Conda (Recommended)
```bash
# Create environment
conda env create -f environment.yml
conda activate resale-flat-analysis

# Test installation
python run_analysis.py
```

#### Using Pip (with Virtual Environment)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Test installation
python run_analysis.py
```

### 3. Quick Test
```bash
# Test API connection (no dependencies required)
python3 demo.py

# Full analysis (requires dependencies)
python run_analysis.py
```

## 📊 Data Source

The project uses Singapore's official resale flat price data from:
- **API Endpoint**: https://data.gov.sg/api/action/datastore_search
- **Dataset ID**: d_8b84c4ee58e3cfc0ece0d773c8ca6abc
- **Data Period**: 2017 onwards
- **Update Frequency**: Monthly

### Data Fields Include:
- Month of sale
- Town
- Flat type
- Block
- Street name
- Storey range
- Floor area (sqm)
- Flat model
- Lease commence date
- Remaining lease
- Resale price

## 🏃‍♂️ Quick Start

### 1. Fetch and Analyze Data
```bash
python data_fetcher.py
```

### 2. Run Streamlit Dashboard
```bash
streamlit run streamlit_app.py
```

### 3. Access Dashboard
Open your browser and navigate to: `http://localhost:8501`

## 📁 Project Structure

```
resale_flat_price_2017_onwards/
├── data_fetcher.py          # Main data fetching and performance comparison
├── streamlit_app.py         # Streamlit dashboard application
├── data_analysis.py         # Data analysis utilities
├── environment.yml          # Conda environment configuration
├── New_Readme.md           # This file
├── readme.md               # Original project notes
├── resale_flat_data.csv    # Cached data (generated)
├── data_metadata.json      # Data metadata (generated)
└── requirements.txt        # Alternative pip requirements
```

## 🔧 Configuration

### Performance Options

The project offers two data access methods:

1. **CSV Storage** (Recommended for analysis)
   - Faster data loading
   - Offline analysis capability
   - Reduced API calls
   - Better for large datasets

2. **Direct API Calls** (Recommended for real-time data)
   - Always up-to-date data
   - Smaller storage requirements
   - Better for small queries
   - Real-time data access

### Environment Variables

You can set the following environment variables:
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

### Dashboard Sections

1. **Data Overview**
   - Dataset summary and statistics
   - Data quality indicators
   - Recent updates information

2. **Price Trends**
   - Historical price trends by town
   - Flat type price comparisons
   - Seasonal patterns analysis

3. **Geographic Analysis**
   - Price heat maps
   - Town-wise price distributions
   - Location-based insights

4. **Predictive Analytics**
   - Price prediction models
   - Market trend forecasting
   - Investment recommendations

5. **Advanced Filters**
   - Multi-dimensional data filtering
   - Custom date ranges
   - Interactive visualizations

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

---

*Last updated: August 2025*
