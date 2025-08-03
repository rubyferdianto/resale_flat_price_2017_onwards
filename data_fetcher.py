"""
Singapore Resale Flat Price Data Fetcher
This module handles data retrieval from data.gov.sg API and provides
options for CSV storage vs direct API calls for performance comparison.
"""

import requests
import pandas as pd
import time
import os
from datetime import datetime
import json


class ResaleFlatDataFetcher:
    """Class to handle resale flat data fetching and storage operations."""
    
    def __init__(self):
        self.dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
        self.base_url = "https://data.gov.sg/api/action/datastore_search"
        self.csv_file = "resale_flat_data.csv"
        
    def fetch_data_from_api(self, limit=100, offset=0):
        """
        Fetch data directly from the API.
        
        Args:
            limit (int): Number of records to fetch per request
            offset (int): Starting position for data fetch
            
        Returns:
            dict: API response data
        """
        url = f"{self.base_url}?resource_id={self.dataset_id}&limit={limit}&offset={offset}"
        
        try:
            start_time = time.time()
            response = requests.get(url)
            response.raise_for_status()
            end_time = time.time()
            
            data = response.json()
            print(f"API call completed in {end_time - start_time:.2f} seconds")
            
            return data
        except requests.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return None
    
    def fetch_all_data(self):
        """
        Fetch all available data from the API in batches.
        
        Returns:
            list: All records from the dataset
        """
        all_records = []
        limit = 1000  # Fetch 1000 records per batch
        offset = 0
        
        print("Fetching all data from API...")
        start_time = time.time()
        
        while True:
            data = self.fetch_data_from_api(limit=limit, offset=offset)
            
            if not data or not data.get('result', {}).get('records'):
                break
                
            records = data['result']['records']
            all_records.extend(records)
            
            print(f"Fetched {len(records)} records (Total: {len(all_records)})")
            
            # Check if we've fetched all available records
            if len(records) < limit:
                break
                
            offset += limit
            
        end_time = time.time()
        print(f"Total fetch time: {end_time - start_time:.2f} seconds")
        print(f"Total records fetched: {len(all_records)}")
        
        return all_records
    
    def save_to_csv(self, data=None):
        """
        Save data to CSV file for faster future access.
        
        Args:
            data (list): Optional data to save. If None, fetches from API.
        """
        if data is None:
            data = self.fetch_all_data()
        
        if not data:
            print("No data to save")
            return False
            
        try:
            df = pd.DataFrame(data)
            df.to_csv(self.csv_file, index=False)
            
            # Add metadata
            metadata = {
                'last_updated': datetime.now().isoformat(),
                'total_records': len(data),
                'columns': list(df.columns)
            }
            
            with open('data_metadata.json', 'w') as f:
                json.dump(metadata, f, indent=2)
                
            print(f"Data saved to {self.csv_file}")
            print(f"Metadata saved to data_metadata.json")
            return True
            
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
            return False
    
    def load_from_csv(self):
        """
        Load data from CSV file.
        
        Returns:
            pandas.DataFrame: Data from CSV file
        """
        try:
            start_time = time.time()
            df = pd.read_csv(self.csv_file)
            end_time = time.time()
            
            print(f"CSV loaded in {end_time - start_time:.2f} seconds")
            print(f"Records in CSV: {len(df)}")
            
            return df
        except FileNotFoundError:
            print(f"CSV file {self.csv_file} not found")
            return None
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return None
    
    def performance_comparison(self):
        """
        Compare performance between API calls and CSV loading.
        """
        print("=== PERFORMANCE COMPARISON ===\n")
        
        # Test API performance
        print("1. Testing API Performance:")
        api_start = time.time()
        sample_data = self.fetch_data_from_api(limit=1000)
        api_end = time.time()
        api_time = api_end - api_start
        print(f"API fetch (1000 records): {api_time:.2f} seconds\n")
        
        # Check if CSV exists, if not create it
        if not os.path.exists(self.csv_file):
            print("2. CSV not found. Creating CSV file...")
            self.save_to_csv()
            print()
        
        # Test CSV performance
        print("3. Testing CSV Performance:")
        csv_start = time.time()
        csv_data = self.load_from_csv()
        csv_end = time.time()
        csv_time = csv_end - csv_start
        
        if csv_data is not None:
            print(f"CSV load (all records): {csv_time:.2f} seconds")
            print(f"Performance improvement: {api_time/csv_time:.2f}x faster\n")
            
            # Recommendations
            print("=== RECOMMENDATIONS ===")
            if csv_time < api_time:
                print("✅ CSV loading is faster for data analysis")
                print("✅ Recommended for repeated data access")
                print("💡 Update CSV periodically to get latest data")
            else:
                print("⚠️  API calls might be better for real-time data")
                print("💡 Consider API calls for small datasets or real-time needs")
        
        return {
            'api_time': api_time,
            'csv_time': csv_time if csv_data is not None else None,
            'csv_records': len(csv_data) if csv_data is not None else 0
        }
    
    def get_data_info(self):
        """Get basic information about the dataset."""
        print("=== DATASET INFORMATION ===")
        
        # Try to get from CSV first
        df = self.load_from_csv()
        
        if df is None:
            # Fallback to API
            print("CSV not available, fetching sample from API...")
            data = self.fetch_data_from_api(limit=10)
            if data and data.get('result', {}).get('records'):
                df = pd.DataFrame(data['result']['records'])
        
        if df is not None:
            print(f"Dataset shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            print("\nSample data:")
            print(df.head())
            print("\nData types:")
            print(df.dtypes)
        else:
            print("Could not retrieve dataset information")


if __name__ == "__main__":
    # Initialize the data fetcher
    fetcher = ResaleFlatDataFetcher()
    
    # Get dataset information
    fetcher.get_data_info()
    
    # Run performance comparison
    fetcher.performance_comparison()
