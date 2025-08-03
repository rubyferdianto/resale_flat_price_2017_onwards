#!/bin/bash

# Singapore Resale Flat Price Analysis Dashboard Launcher
# This script activates the virtual environment and starts the Streamlit dashboard

echo "🏠 Singapore Resale Flat Price Analysis Dashboard"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please set up the environment first:"
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, pandas, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

# Check if data file exists
if [ ! -f "resale_flat_data.csv" ]; then
    echo "⚠️  Data file not found. The app will fetch data from API on first run."
fi

echo "🚀 Starting Streamlit dashboard..."
echo "📱 The dashboard will open in your browser at: http://localhost:8501"
echo ""
echo "💡 Tips:"
echo "   - Use Ctrl+C to stop the dashboard"
echo "   - The first load may take a moment to process data"
echo "   - Use the refresh button in the sidebar to get latest data"
echo ""

# Start Streamlit
streamlit run streamlit_app.py

echo ""
echo "👋 Dashboard stopped. Thank you for using the Singapore Resale Flat Price Analysis!"
