#!/usr/bin/env python3
"""
Simple Demo Script - Singapore Resale Flat Price Data
This script demonstrates the basic API connection and data retrieval.
"""

import requests
import json
import time
from datetime import datetime

def demo_api_connection():
    """Demonstrate API connection to Singapore's resale flat data."""
    print("=" * 60)
    print("SINGAPORE RESALE FLAT PRICE DATA - API DEMO")
    print("=" * 60)
    print()
    
    # API details
    dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
    base_url = "https://data.gov.sg/api/action/datastore_search"
    
    print(f"🌐 API Endpoint: {base_url}")
    print(f"📊 Dataset ID: {dataset_id}")
    print()
    
    # Test basic connection
    print("🔗 Testing API connection...")
    url = f"{base_url}?resource_id={dataset_id}&limit=5"
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=30)
        end_time = time.time()
        
        response.raise_for_status()  # Raise an exception for bad status codes
        
        print(f"✅ Connection successful! ({end_time - start_time:.2f} seconds)")
        
        # Parse response
        data = response.json()
        
        # Display API metadata
        print("\n📋 API Response Information:")
        if 'result' in data:
            result = data['result']
            print(f"   Total records available: {result.get('total', 'Unknown')}")
            print(f"   Records in this response: {len(result.get('records', []))}")
            
            # Display field information
            if 'fields' in result:
                print(f"   Number of fields: {len(result['fields'])}")
                print("\n📊 Available Fields:")
                for i, field in enumerate(result['fields'], 1):
                    field_name = field.get('id', 'Unknown')
                    field_type = field.get('type', 'Unknown')
                    print(f"   {i:2d}. {field_name} ({field_type})")
            
            # Display sample records
            if 'records' in result and result['records']:
                print("\n🔍 Sample Data (First 2 records):")
                for i, record in enumerate(result['records'][:2], 1):
                    print(f"\n   Record {i}:")
                    for key, value in record.items():
                        print(f"      {key}: {value}")
        
        # Test larger dataset fetch
        print("\n🚀 Testing larger data fetch (100 records)...")
        large_url = f"{base_url}?resource_id={dataset_id}&limit=100"
        
        start_time = time.time()
        large_response = requests.get(large_url, timeout=30)
        end_time = time.time()
        
        if large_response.status_code == 200:
            large_data = large_response.json()
            record_count = len(large_data.get('result', {}).get('records', []))
            print(f"✅ Fetched {record_count} records in {end_time - start_time:.2f} seconds")
            
            # Calculate basic statistics
            if record_count > 0:
                records = large_data['result']['records']
                
                # Try to get price statistics
                prices = []
                for record in records:
                    try:
                        price = float(record.get('resale_price', 0))
                        if price > 0:
                            prices.append(price)
                    except (ValueError, TypeError):
                        continue
                
                if prices:
                    print(f"\n📈 Quick Price Statistics (from {len(prices)} valid records):")
                    print(f"   Average price: S${sum(prices)/len(prices):,.0f}")
                    print(f"   Minimum price: S${min(prices):,.0f}")
                    print(f"   Maximum price: S${max(prices):,.0f}")
                
                # Show unique towns and flat types
                towns = set()
                flat_types = set()
                
                for record in records:
                    town = record.get('town', '').strip()
                    flat_type = record.get('flat_type', '').strip()
                    
                    if town:
                        towns.add(town)
                    if flat_type:
                        flat_types.add(flat_type)
                
                if towns:
                    print(f"\n🏘️  Sample Towns ({len(towns)} unique):")
                    print(f"   {', '.join(sorted(list(towns))[:5])}{'...' if len(towns) > 5 else ''}")
                
                if flat_types:
                    print(f"\n🏠 Flat Types ({len(flat_types)} unique):")
                    print(f"   {', '.join(sorted(list(flat_types)))}")
        
        else:
            print(f"❌ Large fetch failed: {large_response.status_code}")
    
    except requests.RequestException as e:
        print(f"❌ Connection failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Performance recommendations
    print("\n" + "=" * 50)
    print("PERFORMANCE RECOMMENDATIONS")
    print("=" * 50)
    print("✅ API Connection: Working properly")
    print("📊 Data Quality: Good (structured JSON response)")
    print("⚡ Speed: Reasonable for small to medium datasets")
    print()
    print("💡 For better performance with large datasets:")
    print("   1. Use CSV caching for repeated analysis")
    print("   2. Implement pagination for large data fetches")
    print("   3. Use data filtering parameters to reduce response size")
    print("   4. Consider scheduled data updates rather than real-time fetching")
    
    print("\n🎯 Next Steps:")
    print("   1. Run 'python setup.py' to install dependencies")
    print("   2. Run 'python run_analysis.py' for full analysis")
    print("   3. Run 'streamlit run streamlit_app.py' for dashboard")
    
    return True

if __name__ == "__main__":
    demo_api_connection()
