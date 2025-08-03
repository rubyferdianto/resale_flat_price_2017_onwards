"""
Comprehensive Singapore Resale Flat Price Analysis Dashboard
Built with Streamlit for interactive data exploration and analysis.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
from data_fetcher import ResaleFlatDataFetcher

# Page configuration
st.set_page_config(
    page_title="Singapore Resale Flat Price Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    """Load data with caching for better performance."""
    fetcher = ResaleFlatDataFetcher()
    
    # Try to load from CSV first
    df = fetcher.load_from_csv()
    
    # If CSV doesn't exist, fetch from API and save
    if df is None:
        st.info("CSV file not found. Fetching data from API... This may take a moment.")
        data = fetcher.fetch_all_data()
        if data:
            fetcher.save_to_csv(data)
            df = pd.DataFrame(data)
        else:
            st.error("Failed to fetch data from API")
            return None
    
    # Data preprocessing
    if df is not None:
        # Convert month to datetime
        df['month'] = pd.to_datetime(df['month'])
        
        # Convert resale_price to numeric
        df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce')
        
        # Convert floor_area_sqm to numeric
        df['floor_area_sqm'] = pd.to_numeric(df['floor_area_sqm'], errors='coerce')
        
        # Calculate price per sqm
        df['price_per_sqm'] = df['resale_price'] / df['floor_area_sqm']
        
        # Extract year from month
        df['year'] = df['month'].dt.year
        
        # Clean up lease_commence_date
        df['lease_commence_date'] = pd.to_numeric(df['lease_commence_date'], errors='coerce')
        
        # Calculate flat age
        current_year = datetime.now().year
        df['flat_age'] = current_year - df['lease_commence_date']
        
    return df

def create_overview_metrics(df):
    """Create overview metrics for the dashboard."""
    if df is None:
        return
        
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Transactions",
            value=f"{len(df):,}"
        )
    
    with col2:
        avg_price = df['resale_price'].mean()
        st.metric(
            label="Average Price",
            value=f"S${avg_price:,.0f}"
        )
    
    with col3:
        avg_price_per_sqm = df['price_per_sqm'].mean()
        st.metric(
            label="Avg Price per sqm",
            value=f"S${avg_price_per_sqm:,.0f}"
        )
    
    with col4:
        date_range = f"{df['month'].min().strftime('%Y-%m')} to {df['month'].max().strftime('%Y-%m')}"
        st.metric(
            label="Data Period",
            value=date_range
        )

def create_price_trends(df):
    """Create price trend visualizations."""
    st.subheader("📈 Price Trends Analysis")
    
    # Monthly average price trend
    monthly_avg = df.groupby('month')['resale_price'].mean().reset_index()
    
    fig = px.line(
        monthly_avg,
        x='month',
        y='resale_price',
        title='Monthly Average Resale Price Trend',
        labels={'resale_price': 'Average Resale Price (S$)', 'month': 'Month'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Price trends by flat type
    col1, col2 = st.columns(2)
    
    with col1:
        flat_type_trends = df.groupby(['month', 'flat_type'])['resale_price'].mean().reset_index()
        fig = px.line(
            flat_type_trends,
            x='month',
            y='resale_price',
            color='flat_type',
            title='Price Trends by Flat Type',
            labels={'resale_price': 'Average Resale Price (S$)', 'month': 'Month'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price distribution by flat type
        fig = px.box(
            df,
            x='flat_type',
            y='resale_price',
            title='Price Distribution by Flat Type'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

def create_geographic_analysis(df):
    """Create geographic analysis visualizations."""
    st.subheader("🗺️ Geographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average price by town
        town_avg = df.groupby('town')['resale_price'].mean().sort_values(ascending=False).head(15)
        
        fig = px.bar(
            x=town_avg.values,
            y=town_avg.index,
            orientation='h',
            title='Top 15 Towns by Average Resale Price',
            labels={'x': 'Average Resale Price (S$)', 'y': 'Town'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Transaction volume by town
        town_volume = df['town'].value_counts().head(15)
        
        fig = px.bar(
            x=town_volume.values,
            y=town_volume.index,
            orientation='h',
            title='Top 15 Towns by Transaction Volume',
            labels={'x': 'Number of Transactions', 'y': 'Town'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

def create_flat_analysis(df):
    """Create flat-specific analysis."""
    st.subheader("🏢 Flat Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price vs Floor Area
        sample_df = df.sample(n=min(5000, len(df)))  # Sample for performance
        fig = px.scatter(
            sample_df,
            x='floor_area_sqm',
            y='resale_price',
            color='flat_type',
            title='Resale Price vs Floor Area',
            labels={'floor_area_sqm': 'Floor Area (sqm)', 'resale_price': 'Resale Price (S$)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price vs Flat Age
        fig = px.scatter(
            sample_df,
            x='flat_age',
            y='resale_price',
            color='flat_type',
            title='Resale Price vs Flat Age',
            labels={'flat_age': 'Flat Age (years)', 'resale_price': 'Resale Price (S$)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

def create_market_insights(df):
    """Create market insights and statistics."""
    st.subheader("💡 Market Insights")
    
    # Calculate year-over-year changes
    yearly_avg = df.groupby('year')['resale_price'].mean()
    yoy_change = yearly_avg.pct_change().iloc[-1] * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="YoY Price Change",
            value=f"{yoy_change:+.1f}%",
            delta=f"{yoy_change:+.1f}%"
        )
    
    with col2:
        most_expensive_town = df.groupby('town')['resale_price'].mean().idxmax()
        most_expensive_price = df.groupby('town')['resale_price'].mean().max()
        st.metric(
            label="Most Expensive Town",
            value=most_expensive_town,
            delta=f"S${most_expensive_price:,.0f}"
        )
    
    with col3:
        most_active_town = df['town'].value_counts().idxmax()
        most_active_count = df['town'].value_counts().iloc[0]
        st.metric(
            label="Most Active Town",
            value=most_active_town,
            delta=f"{most_active_count:,} transactions"
        )
    
    # Market summary
    st.write("### 📊 Market Summary")
    
    # Recent trends (last 12 months)
    recent_data = df[df['month'] >= (df['month'].max() - pd.DateOffset(months=12))]
    
    if len(recent_data) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Recent Price Trends (Last 12 Months)**")
            recent_monthly = recent_data.groupby('month')['resale_price'].mean()
            
            fig = px.line(
                x=recent_monthly.index,
                y=recent_monthly.values,
                title='Recent Monthly Price Trend'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Popular Flat Types (Last 12 Months)**")
            recent_flat_types = recent_data['flat_type'].value_counts()
            
            fig = px.pie(
                values=recent_flat_types.values,
                names=recent_flat_types.index,
                title='Transaction Distribution by Flat Type'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

def create_data_explorer(df):
    """Create interactive data explorer."""
    st.subheader("🔍 Data Explorer")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_towns = st.multiselect(
            "Select Towns",
            options=sorted(df['town'].unique()),
            default=[]
        )
    
    with col2:
        selected_flat_types = st.multiselect(
            "Select Flat Types",
            options=sorted(df['flat_type'].unique()),
            default=[]
        )
    
    with col3:
        price_range = st.slider(
            "Price Range (S$)",
            min_value=int(df['resale_price'].min()),
            max_value=int(df['resale_price'].max()),
            value=(int(df['resale_price'].min()), int(df['resale_price'].max())),
            step=10000
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_towns:
        filtered_df = filtered_df[filtered_df['town'].isin(selected_towns)]
    
    if selected_flat_types:
        filtered_df = filtered_df[filtered_df['flat_type'].isin(selected_flat_types)]
    
    filtered_df = filtered_df[
        (filtered_df['resale_price'] >= price_range[0]) &
        (filtered_df['resale_price'] <= price_range[1])
    ]
    
    if len(filtered_df) > 0:
        st.write(f"**Filtered Results: {len(filtered_df):,} transactions**")
        
        # Display sample data
        st.write("### Sample Data")
        display_columns = ['month', 'town', 'flat_type', 'floor_area_sqm', 'resale_price', 'price_per_sqm']
        st.dataframe(filtered_df[display_columns].head(100))
        
        # Download option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name=f"filtered_resale_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No data matches the selected filters.")

def main():
    """Main Streamlit application."""
    st.markdown('<h1 class="main-header">🏠 Singapore Resale Flat Price Analysis</h1>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data()
    
    if df is None:
        st.error("Failed to load data. Please check your internet connection and try again.")
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Overview", "Price Trends", "Geographic Analysis", "Flat Analysis", "Market Insights", "Data Explorer"]
    )
    
    # Data info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.write("### Data Information")
    st.sidebar.write(f"**Total Records:** {len(df):,}")
    st.sidebar.write(f"**Date Range:** {df['month'].min().strftime('%Y-%m')} to {df['month'].max().strftime('%Y-%m')}")
    st.sidebar.write(f"**Towns:** {df['town'].nunique()}")
    st.sidebar.write(f"**Flat Types:** {df['flat_type'].nunique()}")
    
    # Main content based on selection
    if page == "Overview":
        st.write("## 📊 Dataset Overview")
        create_overview_metrics(df)
        
        # Basic statistics
        st.write("### 📈 Basic Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Price Statistics**")
            price_stats = df['resale_price'].describe()
            st.dataframe(price_stats)
        
        with col2:
            st.write("**Floor Area Statistics**")
            area_stats = df['floor_area_sqm'].describe()
            st.dataframe(area_stats)
    
    elif page == "Price Trends":
        create_price_trends(df)
    
    elif page == "Geographic Analysis":
        create_geographic_analysis(df)
    
    elif page == "Flat Analysis":
        create_flat_analysis(df)
    
    elif page == "Market Insights":
        create_market_insights(df)
    
    elif page == "Data Explorer":
        create_data_explorer(df)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Data source: <a href='https://data.gov.sg'>data.gov.sg</a> | 
            Built with ❤️ using Streamlit | 
            Last updated: {}</p>
        </div>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M")),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
