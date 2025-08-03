#!/usr/bin/env python3
"""
Performance Comparison Runner
This script runs the performance comparison between CSV and API data access methods.
"""

from data_fetcher import ResaleFlatDataFetcher
import time

def main():
    """Run the complete performance analysis."""
    print("=" * 60)
    print("SINGAPORE RESALE FLAT PRICE DATA - PERFORMANCE ANALYSIS")
    print("=" * 60)
    print()
    
    # Initialize fetcher
    fetcher = ResaleFlatDataFetcher()
    
    # Display dataset information
    print("📊 Getting dataset information...")
    fetcher.get_data_info()
    print()
    
    # Run performance comparison
    print("🚀 Running performance comparison...")
    results = fetcher.performance_comparison()
    
    # Display detailed results
    print("\n" + "=" * 50)
    print("DETAILED PERFORMANCE RESULTS")
    print("=" * 50)
    
    if results['csv_time'] is not None:
        print(f"API Response Time: {results['api_time']:.2f} seconds")
        print(f"CSV Load Time: {results['csv_time']:.2f} seconds")
        print(f"Performance Ratio: {results['api_time']/results['csv_time']:.2f}x")
        print(f"CSV Records: {results['csv_records']:,}")
        
        # Calculate recommendations
        if results['csv_time'] < results['api_time']:
            time_saved = results['api_time'] - results['csv_time']
            print(f"Time Saved with CSV: {time_saved:.2f} seconds per load")
        
        print("\n💡 RECOMMENDATIONS:")
        if results['csv_time'] < results['api_time']:
            print("✅ Use CSV for data analysis and visualization")
            print("✅ Update CSV weekly or monthly for fresh data")
            print("✅ CSV is ideal for Streamlit dashboard")
        else:
            print("⚠️  Consider API for real-time requirements")
            print("💡 CSV still recommended for offline analysis")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Run: streamlit run streamlit_app.py")
    print("2. Open browser to: http://localhost:8501")
    print("3. Explore the interactive dashboard")
    
    print("\n📁 FILES CREATED:")
    import os
    files = [
        'resale_flat_data.csv',
        'data_metadata.json'
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # Size in MB
            print(f"✅ {file} ({size:.1f} MB)")
        else:
            print(f"❌ {file} (not created)")

if __name__ == "__main__":
    main()
