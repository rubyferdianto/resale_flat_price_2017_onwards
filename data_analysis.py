"""
Data Analysis Utilities for Singapore Resale Flat Price Analysis
Contains helper functions for data processing and analysis.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json


class ResaleFlatAnalyzer:
    """Class containing analysis utilities for resale flat data."""
    
    def __init__(self, df):
        """
        Initialize analyzer with dataframe.
        
        Args:
            df (pandas.DataFrame): Resale flat data
        """
        self.df = df.copy()
        self.prepare_data()
    
    def prepare_data(self):
        """Prepare and clean data for analysis."""
        # Convert data types
        self.df['month'] = pd.to_datetime(self.df['month'])
        self.df['resale_price'] = pd.to_numeric(self.df['resale_price'], errors='coerce')
        self.df['floor_area_sqm'] = pd.to_numeric(self.df['floor_area_sqm'], errors='coerce')
        self.df['lease_commence_date'] = pd.to_numeric(self.df['lease_commence_date'], errors='coerce')
        
        # Calculate derived fields
        self.df['price_per_sqm'] = self.df['resale_price'] / self.df['floor_area_sqm']
        self.df['year'] = self.df['month'].dt.year
        self.df['quarter'] = self.df['month'].dt.quarter
        
        # Calculate flat age
        current_year = datetime.now().year
        self.df['flat_age'] = current_year - self.df['lease_commence_date']
        
        # Remove outliers (optional)
        self.df = self.remove_outliers()
    
    def remove_outliers(self, method='iqr', factor=1.5):
        """
        Remove outliers from the dataset.
        
        Args:
            method (str): Method to use ('iqr' or 'zscore')
            factor (float): Factor for outlier detection
            
        Returns:
            pandas.DataFrame: Dataset with outliers removed
        """
        df_clean = self.df.copy()
        
        if method == 'iqr':
            # Remove outliers using IQR method
            Q1 = df_clean['resale_price'].quantile(0.25)
            Q3 = df_clean['resale_price'].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - factor * IQR
            upper_bound = Q3 + factor * IQR
            
            df_clean = df_clean[
                (df_clean['resale_price'] >= lower_bound) & 
                (df_clean['resale_price'] <= upper_bound)
            ]
        
        elif method == 'zscore':
            # Remove outliers using Z-score method
            z_scores = np.abs(
                (df_clean['resale_price'] - df_clean['resale_price'].mean()) / 
                df_clean['resale_price'].std()
            )
            df_clean = df_clean[z_scores < factor]
        
        return df_clean
    
    def get_price_trends(self, groupby='month', town=None, flat_type=None):
        """
        Get price trends over time.
        
        Args:
            groupby (str): Time period to group by ('month', 'quarter', 'year')
            town (str): Filter by specific town
            flat_type (str): Filter by specific flat type
            
        Returns:
            pandas.DataFrame: Price trends data
        """
        df_filtered = self.df.copy()
        
        # Apply filters
        if town:
            df_filtered = df_filtered[df_filtered['town'] == town]
        if flat_type:
            df_filtered = df_filtered[df_filtered['flat_type'] == flat_type]
        
        # Group by time period
        if groupby == 'month':
            trends = df_filtered.groupby('month').agg({
                'resale_price': ['mean', 'median', 'count'],
                'price_per_sqm': ['mean', 'median']
            }).round(2)
        elif groupby == 'quarter':
            df_filtered['year_quarter'] = df_filtered['year'].astype(str) + '-Q' + df_filtered['quarter'].astype(str)
            trends = df_filtered.groupby('year_quarter').agg({
                'resale_price': ['mean', 'median', 'count'],
                'price_per_sqm': ['mean', 'median']
            }).round(2)
        elif groupby == 'year':
            trends = df_filtered.groupby('year').agg({
                'resale_price': ['mean', 'median', 'count'],
                'price_per_sqm': ['mean', 'median']
            }).round(2)
        
        # Flatten column names
        trends.columns = ['_'.join(col).strip() for col in trends.columns.values]
        trends = trends.reset_index()
        
        return trends
    
    def get_geographic_analysis(self):
        """
        Get geographic analysis by town.
        
        Returns:
            dict: Geographic analysis results
        """
        town_stats = self.df.groupby('town').agg({
            'resale_price': ['mean', 'median', 'std', 'count'],
            'price_per_sqm': ['mean', 'median'],
            'floor_area_sqm': 'mean'
        }).round(2)
        
        # Flatten column names
        town_stats.columns = ['_'.join(col).strip() for col in town_stats.columns.values]
        town_stats = town_stats.reset_index()
        
        # Sort by average price
        town_stats = town_stats.sort_values('resale_price_mean', ascending=False)
        
        return {
            'town_statistics': town_stats,
            'most_expensive': town_stats.iloc[0]['town'],
            'least_expensive': town_stats.iloc[-1]['town'],
            'highest_volume': town_stats.loc[town_stats['resale_price_count'].idxmax(), 'town']
        }
    
    def get_flat_type_analysis(self):
        """
        Get analysis by flat type.
        
        Returns:
            pandas.DataFrame: Flat type analysis
        """
        flat_stats = self.df.groupby('flat_type').agg({
            'resale_price': ['mean', 'median', 'std', 'count'],
            'price_per_sqm': ['mean', 'median'],
            'floor_area_sqm': 'mean',
            'flat_age': 'mean'
        }).round(2)
        
        # Flatten column names
        flat_stats.columns = ['_'.join(col).strip() for col in flat_stats.columns.values]
        flat_stats = flat_stats.reset_index()
        
        # Sort by average price
        flat_stats = flat_stats.sort_values('resale_price_mean', ascending=False)
        
        return flat_stats
    
    def calculate_price_changes(self, period='yearly'):
        """
        Calculate price changes over time.
        
        Args:
            period (str): Period for calculation ('yearly', 'quarterly', 'monthly')
            
        Returns:
            pandas.DataFrame: Price changes data
        """
        if period == 'yearly':
            price_data = self.df.groupby('year')['resale_price'].mean()
        elif period == 'quarterly':
            self.df['year_quarter'] = self.df['year'].astype(str) + '-Q' + self.df['quarter'].astype(str)
            price_data = self.df.groupby('year_quarter')['resale_price'].mean()
        else:  # monthly
            price_data = self.df.groupby('month')['resale_price'].mean()
        
        # Calculate percentage changes
        price_changes = price_data.pct_change() * 100
        
        return pd.DataFrame({
            'period': price_data.index,
            'average_price': price_data.values,
            'price_change_pct': price_changes.values
        })
    
    def get_market_insights(self):
        """
        Generate market insights and statistics.
        
        Returns:
            dict: Market insights
        """
        recent_6months = self.df[
            self.df['month'] >= (self.df['month'].max() - pd.DateOffset(months=6))
        ]
        
        insights = {
            'total_transactions': len(self.df),
            'total_towns': self.df['town'].nunique(),
            'total_flat_types': self.df['flat_type'].nunique(),
            'date_range': {
                'start': self.df['month'].min().strftime('%Y-%m'),
                'end': self.df['month'].max().strftime('%Y-%m')
            },
            'price_statistics': {
                'mean': self.df['resale_price'].mean(),
                'median': self.df['resale_price'].median(),
                'std': self.df['resale_price'].std(),
                'min': self.df['resale_price'].min(),
                'max': self.df['resale_price'].max()
            },
            'recent_trends': {
                'avg_price_6months': recent_6months['resale_price'].mean(),
                'transaction_count_6months': len(recent_6months),
                'most_active_town_6months': recent_6months['town'].value_counts().index[0] if len(recent_6months) > 0 else None
            }
        }
        
        # Calculate year-over-year change
        if self.df['year'].nunique() > 1:
            yearly_avg = self.df.groupby('year')['resale_price'].mean()
            if len(yearly_avg) > 1:
                yoy_change = ((yearly_avg.iloc[-1] - yearly_avg.iloc[-2]) / yearly_avg.iloc[-2]) * 100
                insights['yoy_price_change'] = yoy_change
        
        return insights
    
    def find_best_deals(self, method='price_per_sqm', top_n=10):
        """
        Find best deals based on different criteria.
        
        Args:
            method (str): Method to use ('price_per_sqm', 'below_median', 'recent_low')
            top_n (int): Number of deals to return
            
        Returns:
            pandas.DataFrame: Best deals
        """
        if method == 'price_per_sqm':
            # Find lowest price per sqm
            deals = self.df.nsmallest(top_n, 'price_per_sqm')
        
        elif method == 'below_median':
            # Find transactions below median for their flat type and town
            median_prices = self.df.groupby(['town', 'flat_type'])['resale_price'].median()
            
            deals_list = []
            for _, row in self.df.iterrows():
                key = (row['town'], row['flat_type'])
                if key in median_prices and row['resale_price'] < median_prices[key]:
                    deals_list.append(row)
            
            if deals_list:
                deals = pd.DataFrame(deals_list).head(top_n)
            else:
                deals = pd.DataFrame()
        
        elif method == 'recent_low':
            # Find recent transactions with low prices
            recent_data = self.df[
                self.df['month'] >= (self.df['month'].max() - pd.DateOffset(months=6))
            ]
            deals = recent_data.nsmallest(top_n, 'resale_price')
        
        return deals
    
    def export_analysis_report(self, filename=None):
        """
        Export comprehensive analysis report to JSON.
        
        Args:
            filename (str): Output filename
            
        Returns:
            dict: Analysis report
        """
        if filename is None:
            filename = f"resale_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'data_period': {
                    'start': self.df['month'].min().isoformat(),
                    'end': self.df['month'].max().isoformat()
                },
                'total_records': len(self.df)
            },
            'market_insights': self.get_market_insights(),
            'geographic_analysis': {
                'town_statistics': self.get_geographic_analysis()['town_statistics'].to_dict('records')
            },
            'flat_type_analysis': self.get_flat_type_analysis().to_dict('records'),
            'price_trends': {
                'yearly': self.get_price_trends('year').to_dict('records'),
                'quarterly': self.get_price_trends('quarter').to_dict('records')
            }
        }
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Analysis report saved to {filename}")
        return report


def main():
    """Example usage of the analyzer."""
    from data_fetcher import ResaleFlatDataFetcher
    
    # Load data
    fetcher = ResaleFlatDataFetcher()
    df = fetcher.load_from_csv()
    
    if df is None:
        print("No data available. Run data_fetcher.py first.")
        return
    
    # Initialize analyzer
    analyzer = ResaleFlatAnalyzer(df)
    
    # Get insights
    insights = analyzer.get_market_insights()
    print("Market Insights:")
    print(f"Total transactions: {insights['total_transactions']:,}")
    print(f"Average price: S${insights['price_statistics']['mean']:,.0f}")
    print(f"Median price: S${insights['price_statistics']['median']:,.0f}")
    
    # Get geographic analysis
    geo_analysis = analyzer.get_geographic_analysis()
    print(f"\nMost expensive town: {geo_analysis['most_expensive']}")
    print(f"Most active town: {geo_analysis['highest_volume']}")
    
    # Export report
    analyzer.export_analysis_report()


if __name__ == "__main__":
    main()
